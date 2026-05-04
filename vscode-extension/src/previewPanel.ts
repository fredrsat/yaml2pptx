import * as vscode from 'vscode';
import * as yaml from 'js-yaml';

export class PreviewPanel {
    public static currentPanel: PreviewPanel | undefined;
    private static readonly viewType = 'yaml2pptxPreview';

    private readonly panel: vscode.WebviewPanel;
    private readonly extensionUri: vscode.Uri;
    private disposables: vscode.Disposable[] = [];

    public static createOrShow(extensionUri: vscode.Uri, document: vscode.TextDocument) {
        const column = vscode.ViewColumn.Beside;

        if (PreviewPanel.currentPanel) {
            PreviewPanel.currentPanel.panel.reveal(column);
            PreviewPanel.currentPanel.update(document);
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

        PreviewPanel.currentPanel = new PreviewPanel(panel, extensionUri);
        PreviewPanel.currentPanel.update(document);
    }

    public static updateIfActive(document: vscode.TextDocument) {
        if (PreviewPanel.currentPanel) {
            PreviewPanel.currentPanel.update(document);
        }
    }

    private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri) {
        this.panel = panel;
        this.extensionUri = extensionUri;

        this.panel.onDidDispose(() => this.dispose(), null, this.disposables);
    }

    public update(document: vscode.TextDocument) {
        const text = document.getText();
        let slidesJson = '[]';
        let metadataJson = '{}';
        let themeConfigJson = '{}';
        let error = '';

        try {
            const data = yaml.load(text) as Record<string, unknown> | null;
            if (!data || typeof data !== 'object' || !('slides' in data)) {
                error = 'No slides found in YAML file.';
            } else {
                slidesJson = JSON.stringify(data.slides || []);
                metadataJson = JSON.stringify(data.metadata || {});
                themeConfigJson = JSON.stringify(data.theme_config || {});
            }
        } catch (e: unknown) {
            error = 'YAML parse error: ' + (e instanceof Error ? e.message : String(e));
        }

        this.panel.webview.html = this.getHtml(slidesJson, metadataJson, themeConfigJson, error);
    }

    private dispose() {
        PreviewPanel.currentPanel = undefined;
        this.panel.dispose();
        while (this.disposables.length) {
            const d = this.disposables.pop();
            if (d) { d.dispose(); }
        }
    }

    private getHtml(slidesJson: string, metadataJson: string, themeConfigJson: string, error: string): string {
        const webview = this.panel.webview;
        const jsUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this.extensionUri, 'media', 'preview.js')
        );

        // Encode as base64 to avoid any script/HTML escaping issues
        const payload = JSON.stringify({
            slides: JSON.parse(slidesJson),
            metadata: JSON.parse(metadataJson),
            themeConfig: JSON.parse(themeConfigJson),
            error: error,
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
