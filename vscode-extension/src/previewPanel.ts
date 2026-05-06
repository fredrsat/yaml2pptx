import * as vscode from 'vscode';
import * as yaml from 'js-yaml';
import * as path from 'path';

export class PreviewPanel {
    public static currentPanel: PreviewPanel | undefined;
    private static readonly viewType = 'yaml2pptxPreview';

    private readonly panel: vscode.WebviewPanel;
    private readonly extensionUri: vscode.Uri;
    private disposables: vscode.Disposable[] = [];
    private debounceTimer: ReturnType<typeof setTimeout> | undefined;
    private ready = false;

    public static createOrShow(extensionUri: vscode.Uri, document: vscode.TextDocument) {
        const column = vscode.ViewColumn.Beside;

        if (PreviewPanel.currentPanel) {
            PreviewPanel.currentPanel.panel.reveal(column);
            PreviewPanel.currentPanel.sendUpdate(document);
            return;
        }

        const panel = vscode.window.createWebviewPanel(
            PreviewPanel.viewType,
            'yaml2pptx Preview',
            column,
            {
                enableScripts: true,
                localResourceRoots: [vscode.Uri.joinPath(extensionUri, 'media')],
                retainContextWhenHidden: true,
            }
        );

        PreviewPanel.currentPanel = new PreviewPanel(panel, extensionUri, document);
    }

    public static updateIfActive(document: vscode.TextDocument) {
        if (PreviewPanel.currentPanel) {
            PreviewPanel.currentPanel.debouncedUpdate(document);
        }
    }

    private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri, initialDocument: vscode.TextDocument) {
        this.panel = panel;
        this.extensionUri = extensionUri;

        this.panel.onDidDispose(() => this.dispose(), null, this.disposables);

        // Listen for ready message from webview
        this.panel.webview.onDidReceiveMessage(
            message => {
                if (message.type === 'ready') {
                    this.ready = true;
                    this.sendUpdate(initialDocument);
                }
            },
            null,
            this.disposables
        );

        // Set initial HTML with inline data as fallback
        this.panel.webview.html = this.getHtml(initialDocument);
    }

    private debouncedUpdate(document: vscode.TextDocument) {
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        this.debounceTimer = setTimeout(() => {
            this.sendUpdate(document);
        }, 300);
    }

    private sendUpdate(document: vscode.TextDocument) {
        const parsed = this.parseYaml(document);
        if (!parsed) { return; }

        // Update panel title
        const fileName = path.basename(document.uri.fsPath);
        this.panel.title = `Preview: ${fileName}`;

        this.panel.webview.postMessage({
            type: 'update',
            slides: parsed.slides,
            metadata: parsed.metadata,
            themeConfig: parsed.themeConfig,
            theme: parsed.theme,
        });
    }

    private parseYaml(document: vscode.TextDocument): { slides: unknown[]; metadata: object; themeConfig: object; theme: string } | null {
        try {
            const data = yaml.load(document.getText()) as Record<string, unknown> | null;
            if (!data || typeof data !== 'object' || !('slides' in data)) {
                return null;
            }
            return {
                slides: (data.slides as unknown[]) || [],
                metadata: (data.metadata as object) || {},
                themeConfig: (data.theme_config as object) || {},
                theme: (data.theme as string) || 'default',
            };
        } catch {
            return null;
        }
    }

    private dispose() {
        PreviewPanel.currentPanel = undefined;
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        this.panel.dispose();
        while (this.disposables.length) {
            const d = this.disposables.pop();
            if (d) { d.dispose(); }
        }
    }

    private getHtml(document: vscode.TextDocument): string {
        const webview = this.panel.webview;
        const jsUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this.extensionUri, 'media', 'preview.js')
        );

        // Embed initial data as base64 for first render
        const parsed = this.parseYaml(document);
        const payload = JSON.stringify({
            slides: parsed ? parsed.slides : [],
            metadata: parsed ? parsed.metadata : {},
            themeConfig: parsed ? parsed.themeConfig : {},
            theme: parsed ? parsed.theme : 'default',
            error: parsed ? '' : 'No slides found in YAML file.',
        });
        const b64 = Buffer.from(payload, 'utf-8').toString('base64');

        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>yaml2pptx Preview</title>
</head>
<body>
    <div id="app"></div>
    <div id="__data" style="display:none;">${b64}</div>
    <script src="${jsUri}"></script>
</body>
</html>`;
    }
}
