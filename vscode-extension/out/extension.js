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
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const previewPanel_1 = require("./previewPanel");
function activate(context) {
    // Register preview command
    context.subscriptions.push(vscode.commands.registerCommand('yaml2pptx.preview', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor || editor.document.languageId !== 'yaml') {
            vscode.window.showWarningMessage('Open a YAML file first.');
            return;
        }
        previewPanel_1.PreviewPanel.createOrShow(context.extensionUri, editor.document);
    }));
    // Register generate command
    context.subscriptions.push(vscode.commands.registerCommand('yaml2pptx.generate', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor || editor.document.languageId !== 'yaml') {
            vscode.window.showWarningMessage('Open a YAML file first.');
            return;
        }
        const filePath = editor.document.uri.fsPath;
        const terminal = vscode.window.createTerminal('yaml2pptx');
        terminal.show();
        terminal.sendText(`yaml2pptx build "${filePath}" --open`);
    }));
    // Watch for text changes to update preview
    context.subscriptions.push(vscode.workspace.onDidChangeTextDocument(e => {
        if (e.document.languageId === 'yaml') {
            previewPanel_1.PreviewPanel.updateIfActive(e.document);
        }
    }));
    // Watch for active editor changes
    context.subscriptions.push(vscode.window.onDidChangeActiveTextEditor(editor => {
        if (editor && editor.document.languageId === 'yaml') {
            previewPanel_1.PreviewPanel.updateIfActive(editor.document);
        }
    }));
}
function deactivate() { }
//# sourceMappingURL=extension.js.map