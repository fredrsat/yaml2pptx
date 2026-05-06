import * as vscode from 'vscode';
import { PreviewPanel } from './previewPanel';

export function activate(context: vscode.ExtensionContext) {
    // Register preview command
    context.subscriptions.push(
        vscode.commands.registerCommand('yaml2pptx.preview', () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor || editor.document.languageId !== 'yaml') {
                vscode.window.showWarningMessage('Open a YAML file first.');
                return;
            }
            PreviewPanel.createOrShow(context.extensionUri, editor.document);
        })
    );

    // Register generate command
    context.subscriptions.push(
        vscode.commands.registerCommand('yaml2pptx.generate', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor || editor.document.languageId !== 'yaml') {
                vscode.window.showWarningMessage('Open a YAML file first.');
                return;
            }

            const filePath = editor.document.uri.fsPath;
            const terminal = vscode.window.createTerminal('yaml2pptx');
            terminal.show();
            terminal.sendText(`yaml2pptx build "${filePath}" --open || echo "Error: yaml2pptx not found. Install with: pip install -e ."`);
        })
    );

    // Watch for text changes to update preview
    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(e => {
            if (e.document.languageId === 'yaml') {
                PreviewPanel.updateIfActive(e.document);
            }
        })
    );

    // Watch for active editor changes
    context.subscriptions.push(
        vscode.window.onDidChangeActiveTextEditor(editor => {
            if (editor && editor.document.languageId === 'yaml') {
                PreviewPanel.updateIfActive(editor.document);
            }
        })
    );
}

export function deactivate() {}
