"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.PreviewPanel = void 0;
const vscode = __importStar(require("vscode"));
const yaml = __importStar(require("js-yaml"));
class PreviewPanel {
    static currentPanel;
    static viewType = 'yaml2pptxPreview';
    panel;
    extensionUri;
    disposables = [];
    static createOrShow(extensionUri, document) {
        const column = vscode.ViewColumn.Beside;
        if (PreviewPanel.currentPanel) {
            PreviewPanel.currentPanel.panel.reveal(column);
            PreviewPanel.currentPanel.update(document);
            return;
        }
        const panel = vscode.window.createWebviewPanel(PreviewPanel.viewType, 'yaml2pptx Preview', column, {
            enableScripts: true,
            localResourceRoots: [vscode.Uri.joinPath(extensionUri, 'media')],
            retainContextWhenHidden: true,
        });
        PreviewPanel.currentPanel = new PreviewPanel(panel, extensionUri);
        PreviewPanel.currentPanel.update(document);
    }
    static updateIfActive(document) {
        if (PreviewPanel.currentPanel) {
            PreviewPanel.currentPanel.update(document);
        }
    }
    constructor(panel, extensionUri) {
        this.panel = panel;
        this.extensionUri = extensionUri;
        this.panel.onDidDispose(() => this.dispose(), null, this.disposables);
    }
    update(document) {
        const text = document.getText();
        let slidesJson = '[]';
        let metadataJson = '{}';
        let themeConfigJson = '{}';
        let error = '';
        try {
            const data = yaml.load(text);
            if (!data || typeof data !== 'object' || !('slides' in data)) {
                error = 'No slides found in YAML file.';
            }
            else {
                slidesJson = JSON.stringify(data.slides || []);
                metadataJson = JSON.stringify(data.metadata || {});
                themeConfigJson = JSON.stringify(data.theme_config || {});
            }
        }
        catch (e) {
            error = 'YAML parse error: ' + (e instanceof Error ? e.message : String(e));
        }
        this.panel.webview.html = this.getHtml(slidesJson, metadataJson, themeConfigJson, error);
    }
    dispose() {
        PreviewPanel.currentPanel = undefined;
        this.panel.dispose();
        while (this.disposables.length) {
            const d = this.disposables.pop();
            if (d) {
                d.dispose();
            }
        }
    }
    getHtml(slidesJson, metadataJson, themeConfigJson, error) {
        const webview = this.panel.webview;
        const jsUri = webview.asWebviewUri(vscode.Uri.joinPath(this.extensionUri, 'media', 'preview.js'));
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
exports.PreviewPanel = PreviewPanel;
//# sourceMappingURL=previewPanel.js.map