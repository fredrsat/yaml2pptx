// yaml2pptx VS Code Webview Preview Script
// Renders slide data as HTML inside a VS Code webview panel.

(function () {
    'use strict';

    const vscode = acquireVsCodeApi();

    // --- Theme ---
    const THEME = {
        primary: '#003087',
        accent: '#00A9A5',
        lightBlue: '#6CACE4',
        darkNavy: '#001F5C',
        textDark: '#1F2937',
        textMuted: '#64748B',
        textLight: '#9CA3AF',
        white: '#FFFFFF',
        cardBg: '#F8FAFC',
        success: '#059669',
        warning: '#E87722',
        font: 'Calibri, sans-serif',
    };

    // --- State ---
    let currentSlideIndex = 0;
    let slides = [];
    let metadata = {};
    let themeConfig = {};

    // --- Inline Markdown parser ---
    function parseMarkdown(text) {
        if (text == null) return '';
        text = String(text);
        // Bold: **text**
        text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        // Strikethrough: ~~text~~
        text = text.replace(/~~(.+?)~~/g, '<del>$1</del>');
        // Italic: *text* (but not inside already-processed strong tags)
        text = text.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, '<em>$1</em>');
        // Code: `text`
        text = text.replace(/`(.+?)`/g, '<code style="background:#E2E8F0;padding:1px 4px;border-radius:3px;font-size:0.9em;">$1</code>');
        // Links: [text](url)
        text = text.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" style="color:' + THEME.accent + ';">$1</a>');
        return text;
    }

    // --- Escape HTML ---
    function esc(text) {
        if (text == null) return '';
        return String(text)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    // Parse markdown on already-escaped text is wrong; we need to parse markdown on raw text.
    // So: parseMarkdown expects raw text and handles it. We trust the YAML content.
    // For user-facing text we use parseMarkdown directly (which does not escape HTML first,
    // since presentation content may intentionally contain markup-like patterns).

    // --- Helper: safe text with markdown ---
    function md(text) {
        return parseMarkdown(text);
    }

    // --- Helper: render bullet list ---
    function renderBulletList(items, options) {
        if (!items || !items.length) return '';
        const opts = options || {};
        const color = opts.color || THEME.textDark;
        const bulletColor = opts.bulletColor || THEME.accent;
        let html = '<ul style="list-style:none;padding:0;margin:4px 0;">';
        for (const item of items) {
            const text = typeof item === 'string' ? item : (item.text || '');
            const level = (typeof item === 'object' && item.level) ? item.level : 0;
            const indent = level * 20;
            html += '<li style="padding:2px 0;padding-left:' + (12 + indent) + 'px;color:' + color + ';font-size:0.72em;position:relative;">';
            html += '<span style="position:absolute;left:' + indent + 'px;color:' + bulletColor + ';">&bull;</span>';
            html += md(text);
            html += '</li>';
        }
        html += '</ul>';
        return html;
    }

    // --- Common header for non-title slides ---
    function renderSlideHeader(slide, index) {
        const section = slide.section || '';
        const pageNum = index + 1;
        return '<div style="display:flex;align-items:center;justify-content:space-between;padding:12px 20px 8px 20px;">'
            + '<div style="display:flex;align-items:center;gap:8px;">'
            + '<div style="width:10px;height:10px;background:' + THEME.accent + ';"></div>'
            + '<span style="font-size:0.6em;text-transform:uppercase;letter-spacing:1px;color:' + THEME.textMuted + ';">' + esc(section) + '</span>'
            + '</div>'
            + '<span style="font-size:0.6em;color:' + THEME.textMuted + ';">' + pageNum + '</span>'
            + '</div>';
    }

    // --- Common footer ---
    function renderSlideFooter(slide) {
        const org = (themeConfig && themeConfig.organization) || '';
        if (!org) return '';
        return '<div style="position:absolute;bottom:6px;left:20px;right:20px;font-size:0.5em;color:' + THEME.textLight + ';border-top:1px solid #E2E8F0;padding-top:4px;">'
            + esc(org)
            + '</div>';
    }

    // --- Speaker notes badge ---
    function renderNotesBadge(slide) {
        if (!slide.speaker_notes) return '';
        return '<div style="position:absolute;bottom:8px;right:8px;background:' + THEME.accent + ';color:white;font-size:0.5em;padding:2px 6px;border-radius:3px;opacity:0.8;" title="' + esc(slide.speaker_notes) + '">Notes</div>';
    }

    // --- Icon placeholder ---
    function renderIcon(iconName, size, bgColor) {
        size = size || 28;
        bgColor = bgColor || THEME.accent;
        return '<div style="width:' + size + 'px;height:' + size + 'px;background:' + bgColor + ';border-radius:4px;display:flex;align-items:center;justify-content:center;color:white;font-size:' + (size * 0.4) + 'px;flex-shrink:0;" title="' + esc(iconName || '') + '">'
            + (iconName ? esc(iconName).substring(0, 2) : '?')
            + '</div>';
    }

    // =============================================
    // Slide type renderers
    // =============================================

    function renderTitlePage(slide, index) {
        const category = slide.category || '';
        const title = slide.title || '';
        const subtitle = slide.subtitle || '';
        const author = slide.author || (metadata && metadata.author) || '';
        const date = slide.date || '';
        return '<div style="background:' + THEME.darkNavy + ';color:white;height:100%;display:flex;flex-direction:column;justify-content:center;padding:30px 40px;position:relative;overflow:hidden;">'
            + '<div style="position:absolute;top:16px;left:16px;width:20px;height:20px;background:' + THEME.accent + ';"></div>'
            + (category ? '<div style="font-size:0.6em;text-transform:uppercase;letter-spacing:2px;color:' + THEME.lightBlue + ';margin-bottom:8px;">' + esc(category) + '</div>' : '')
            + '<div style="font-size:2.5em;font-weight:700;line-height:1.1;margin-bottom:10px;">' + md(title) + '</div>'
            + (subtitle ? '<div style="font-size:1em;color:' + THEME.lightBlue + ';margin-bottom:20px;">' + md(subtitle) + '</div>' : '')
            + '<div style="width:40px;height:2px;background:' + THEME.accent + ';margin-bottom:12px;"></div>'
            + '<div style="font-size:0.7em;color:' + THEME.textLight + ';">'
            + (author ? esc(author) : '') + (author && date ? ' &middot; ' : '') + (date ? esc(date) : '')
            + '</div>'
            + renderNotesBadge(slide)
            + '</div>';
    }

    function renderAgenda(slide, index) {
        const items = slide.items || [];
        let itemsHtml = '';
        for (let i = 0; i < items.length; i++) {
            const item = items[i];
            if (i > 0) {
                itemsHtml += '<div style="border-top:1px solid #E2E8F0;margin:4px 0;"></div>';
            }
            itemsHtml += '<div style="display:flex;align-items:flex-start;gap:12px;padding:4px 0;">'
                + '<div style="font-size:1.6em;font-weight:700;color:' + THEME.accent + ';min-width:30px;">' + String(i + 1).padStart(2, '0') + '</div>'
                + '<div>'
                + '<div style="font-weight:600;font-size:0.8em;color:' + THEME.textDark + ';">' + md(item.title || '') + '</div>'
                + (item.description ? '<div style="font-size:0.65em;color:' + THEME.textMuted + ';margin-top:2px;">' + md(item.description) + '</div>' : '')
                + '</div>'
                + '</div>';
        }
        return renderSlideHeader(slide, index)
            + '<div style="padding:4px 20px 20px 20px;">'
            + '<div style="font-size:1.2em;font-weight:700;color:' + THEME.textDark + ';margin-bottom:10px;">' + md(slide.title || '') + '</div>'
            + itemsHtml
            + '</div>'
            + renderSlideFooter(slide)
            + renderNotesBadge(slide);
    }

    function renderStatCards(slide, index) {
        const cards = slide.cards || [];
        let cardsHtml = '<div style="display:flex;gap:10px;flex-wrap:wrap;">';
        for (const card of cards) {
            cardsHtml += '<div style="flex:1;min-width:80px;background:' + THEME.cardBg + ';border-top:3px solid ' + THEME.accent + ';padding:10px;border-radius:4px;">'
                + '<div style="font-size:2em;font-weight:700;color:' + THEME.accent + ';line-height:1;">' + esc(card.stat || '') + '</div>'
                + (card.label ? '<div style="font-size:0.55em;color:' + THEME.textLight + ';text-transform:uppercase;letter-spacing:1px;margin-top:2px;">' + esc(card.label) + '</div>' : '')
                + (card.title ? '<div style="font-size:0.7em;font-weight:600;color:' + THEME.textDark + ';margin-top:6px;">' + md(card.title) + '</div>' : '')
                + (card.description ? '<div style="font-size:0.6em;color:' + THEME.textMuted + ';margin-top:2px;">' + md(card.description) + '</div>' : '')
                + '</div>';
        }
        cardsHtml += '</div>';
        return renderSlideHeader(slide, index)
            + '<div style="padding:4px 20px 20px 20px;">'
            + '<div style="font-size:1.2em;font-weight:700;color:' + THEME.textDark + ';margin-bottom:10px;">' + md(slide.title || '') + '</div>'
            + cardsHtml
            + '</div>'
            + renderSlideFooter(slide)
            + renderNotesBadge(slide);
    }

    function renderDefinitionCards(slide, index) {
        const cards = slide.cards || [];
        let cardsHtml = '<div style="display:flex;gap:10px;flex-wrap:wrap;">';
        for (const card of cards) {
            const borderColor = card.color || THEME.primary;
            cardsHtml += '<div style="flex:1;min-width:100px;background:' + THEME.cardBg + ';border-top:3px solid ' + borderColor + ';padding:10px;border-radius:4px;">'
                + (card.icon ? '<div style="margin-bottom:6px;">' + renderIcon(card.icon, 24, borderColor) + '</div>' : '')
                + '<div style="font-size:0.95em;font-weight:700;color:' + THEME.textDark + ';">' + md(card.term || '') + '</div>'
                + (card.subtitle ? '<div style="font-size:0.6em;color:' + THEME.textMuted + ';margin-top:2px;">' + md(card.subtitle) + '</div>' : '')
                + (card.description ? '<div style="font-size:0.65em;color:' + THEME.textDark + ';margin-top:6px;">' + md(card.description) + '</div>' : '')
                + '</div>';
        }
        cardsHtml += '</div>';
        let calloutHtml = '';
        if (slide.callout) {
            calloutHtml = '<div style="background:' + THEME.darkNavy + ';color:white;padding:8px 14px;border-radius:4px;margin-top:10px;font-size:0.65em;">' + md(slide.callout) + '</div>';
        }
        return renderSlideHeader(slide, index)
            + '<div style="padding:4px 20px 20px 20px;">'
            + '<div style="font-size:1.2em;font-weight:700;color:' + THEME.textDark + ';margin-bottom:10px;">' + md(slide.title || '') + '</div>'
            + cardsHtml
            + calloutHtml
            + '</div>'
            + renderSlideFooter(slide)
            + renderNotesBadge(slide);
    }

    function renderContentCards(slide, index) {
        const cards = slide.cards || [];
        let cardsHtml = '<div style="display:flex;gap:10px;flex-wrap:wrap;">';
        for (const card of cards) {
            cardsHtml += '<div style="flex:1;min-width:100px;background:' + THEME.cardBg + ';border-top:3px solid ' + THEME.primary + ';padding:10px;border-radius:4px;">'
                + (card.icon ? '<div style="margin-bottom:6px;">' + renderIcon(card.icon, 24) + '</div>' : '')
                + '<div style="font-size:0.8em;font-weight:600;color:' + THEME.textDark + ';">' + md(card.title || '') + '</div>'
                + (card.subtitle ? '<div style="font-size:0.6em;color:' + THEME.textMuted + ';margin-top:2px;">' + md(card.subtitle) + '</div>' : '')
                + renderBulletList(card.points || [])
                + '</div>';
        }
        cardsHtml += '</div>';
        return renderSlideHeader(slide, index)
            + '<div style="padding:4px 20px 20px 20px;">'
            + '<div style="font-size:1.2em;font-weight:700;color:' + THEME.textDark + ';margin-bottom:10px;">' + md(slide.title || '') + '</div>'
            + cardsHtml
            + '</div>'
            + renderSlideFooter(slide)
            + renderNotesBadge(slide);
    }

    function renderIconCards(slide, index) {
        const cards = slide.cards || [];
        const message = slide.message || '';
        let cardsHtml = '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;">';
        for (const card of cards) {
            cardsHtml += '<div style="flex:1;min-width:100px;background:white;border-left:3px solid ' + THEME.accent + ';padding:10px;border-radius:0 4px 4px 0;">'
                + '<div style="display:flex;align-items:flex-start;gap:8px;">'
                + renderIcon(card.icon, 24)
                + '<div>'
                + '<div style="font-size:0.75em;font-weight:600;color:' + THEME.textDark + ';">' + md(card.title || '') + '</div>'
                + (card.description ? '<div style="font-size:0.6em;color:' + THEME.textMuted + ';margin-top:2px;">' + md(card.description) + '</div>' : '')
                + '</div>'
                + '</div>'
                + '</div>';
        }
        cardsHtml += '</div>';
        return renderSlideHeader(slide, index)
            + '<div style="padding:4px 20px 20px 20px;">'
            + (message ? '<div style="font-size:1.1em;font-weight:700;color:' + THEME.accent + ';margin-bottom:6px;">' + md(message) + '</div>' : '')
            + cardsHtml
            + '</div>'
            + renderSlideFooter(slide)
            + renderNotesBadge(slide);
    }

    function renderTwoPanels(slide, index) {
        const left = slide.left_panel || {};
        const right = slide.right_panel || {};

        function panelHtml(panel, isDark) {
            const bg = isDark ? THEME.darkNavy : THEME.cardBg;
            const textColor = isDark ? THEME.white : THEME.textDark;
            const mutedColor = isDark ? THEME.lightBlue : THEME.textMuted;
            return '<div style="flex:1;background:' + bg + ';padding:14px;border-radius:4px;color:' + textColor + ';">'
                + (panel.letter ? '<div style="font-size:1.8em;font-weight:700;color:' + THEME.accent + ';line-height:1;">' + esc(panel.letter) + '</div>' : '')
                + (panel.label ? '<div style="font-size:0.55em;text-transform:uppercase;letter-spacing:1px;color:' + mutedColor + ';margin-top:2px;">' + esc(panel.label) + '</div>' : '')
                + (panel.title ? '<div style="font-size:0.8em;font-weight:600;margin-top:6px;">' + md(panel.title) + '</div>' : '')
                + (panel.example ? '<div style="font-size:0.65em;font-style:italic;color:' + mutedColor + ';margin-top:4px;">' + md(panel.example) + '</div>' : '')
                + renderBulletList(panel.points || [], { color: textColor, bulletColor: THEME.accent })
                + '</div>';
        }

        return renderSlideHeader(slide, index)
            + '<div style="padding:4px 20px 20px 20px;">'
            + '<div style="font-size:1.2em;font-weight:700;color:' + THEME.textDark + ';margin-bottom:10px;">' + md(slide.title || '') + '</div>'
            + '<div style="display:flex;gap:10px;">'
            + panelHtml(left, true)
            + panelHtml(right, false)
            + '</div>'
            + '</div>'
            + renderSlideFooter(slide)
            + renderNotesBadge(slide);
    }

    function renderComparison(slide, index) {
        const left = slide.left_panel || {};
        const right = slide.right_panel || {};

        function panelHtml(panel, headerBg) {
            let rowsHtml = '';
            const rows = panel.rows || [];
            for (const row of rows) {
                rowsHtml += '<div style="display:flex;gap:8px;padding:4px 0;border-bottom:1px solid #E2E8F0;font-size:0.65em;">'
                    + '<div style="font-weight:600;color:' + headerBg + ';min-width:60px;">' + md(row.label || '') + '</div>'
                    + '<div style="color:' + THEME.textDark + ';">' + md(row.value || '') + '</div>'
                    + '</div>';
            }
            return '<div style="flex:1;border-radius:4px;overflow:hidden;background:white;">'
                + '<div style="background:' + headerBg + ';color:white;padding:6px 10px;font-size:0.7em;font-weight:600;">' + esc(panel.header || '') + '</div>'
                + '<div style="padding:8px 10px;">'
                + (panel.title ? '<div style="font-size:0.75em;font-weight:600;color:' + THEME.textDark + ';margin-bottom:6px;">' + md(panel.title) + '</div>' : '')
                + rowsHtml
                + '</div>'
                + '</div>';
        }

        return renderSlideHeader(slide, index)
            + '<div style="padding:4px 20px 20px 20px;">'
            + '<div style="font-size:1.2em;font-weight:700;color:' + THEME.textDark + ';margin-bottom:10px;">' + md(slide.title || '') + '</div>'
            + '<div style="display:flex;gap:10px;">'
            + panelHtml(left, THEME.primary)
            + panelHtml(right, THEME.accent)
            + '</div>'
            + '</div>'
            + renderSlideFooter(slide)
            + renderNotesBadge(slide);
    }

    function renderSectionDivider(slide, index) {
        return '<div style="background:' + THEME.darkNavy + ';color:white;height:100%;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;padding:30px 40px;position:relative;">'
            + (slide.number != null ? '<div style="font-size:5em;font-weight:700;color:' + THEME.accent + ';line-height:1;opacity:0.9;">' + esc(String(slide.number)) + '</div>' : '')
            + '<div style="font-size:2em;font-weight:700;margin-top:6px;">' + md(slide.title || '') + '</div>'
            + (slide.subtitle ? '<div style="font-size:0.9em;color:' + THEME.lightBlue + ';margin-top:6px;">' + md(slide.subtitle) + '</div>' : '')
            + renderNotesBadge(slide)
            + '</div>';
    }

    function renderTimeline(slide, index) {
        const phases = slide.phases || [];
        const count = phases.length;
        let nodesHtml = '<div style="display:flex;align-items:flex-start;gap:0;margin-top:10px;position:relative;">';

        for (let i = 0; i < count; i++) {
            const phase = phases[i];
            const isActive = phase.active || (i === 0 && !phases.some(function (p) { return p.active; }));
            const nodeColor = isActive ? THEME.accent : THEME.textLight;

            nodesHtml += '<div style="flex:1;display:flex;flex-direction:column;align-items:center;position:relative;">';
            // Label above
            nodesHtml += '<div style="font-size:0.55em;color:' + nodeColor + ';font-weight:600;margin-bottom:6px;text-align:center;">' + esc(phase.label || '') + '</div>';
            // Node
            nodesHtml += '<div style="width:16px;height:16px;border-radius:50%;background:' + nodeColor + ';z-index:1;position:relative;"></div>';
            // Connector line (not after last)
            if (i < count - 1) {
                nodesHtml += '<div style="position:absolute;top:calc(0.55em + 6px + 7px);left:calc(50% + 8px);right:calc(-50% + 8px);height:2px;background:' + THEME.textLight + ';z-index:0;width:calc(100% - 16px);"></div>';
            }
            // Title + content below
            nodesHtml += '<div style="margin-top:8px;text-align:center;">';
            nodesHtml += '<div style="font-size:0.7em;font-weight:600;color:' + THEME.textDark + ';">' + md(phase.title || '') + '</div>';
            if (phase.description) {
                nodesHtml += '<div style="font-size:0.55em;color:' + THEME.textMuted + ';margin-top:2px;">' + md(phase.description) + '</div>';
            }
            if (phase.items && phase.items.length) {
                nodesHtml += '<div style="font-size:0.55em;color:' + THEME.textMuted + ';margin-top:2px;text-align:left;display:inline-block;">';
                for (const item of phase.items) {
                    nodesHtml += '<div>&bull; ' + md(typeof item === 'string' ? item : item.text || '') + '</div>';
                }
                nodesHtml += '</div>';
            }
            nodesHtml += '</div>';
            nodesHtml += '</div>';
        }

        nodesHtml += '</div>';

        return renderSlideHeader(slide, index)
            + '<div style="padding:4px 20px 20px 20px;">'
            + '<div style="font-size:1.2em;font-weight:700;color:' + THEME.textDark + ';margin-bottom:6px;">' + md(slide.title || '') + '</div>'
            + nodesHtml
            + '</div>'
            + renderSlideFooter(slide)
            + renderNotesBadge(slide);
    }

    function renderProcess(slide, index) {
        const steps = slide.steps || [];
        let stepsHtml = '<div style="display:flex;align-items:flex-start;gap:6px;flex-wrap:wrap;">';

        for (let i = 0; i < steps.length; i++) {
            const step = steps[i];
            // Arrow between steps
            if (i > 0) {
                stepsHtml += '<div style="display:flex;align-items:center;padding-top:20px;color:' + THEME.textLight + ';font-size:1.2em;">&rarr;</div>';
            }
            stepsHtml += '<div style="flex:1;min-width:80px;background:' + THEME.cardBg + ';padding:10px;border-radius:4px;text-align:center;">'
                + '<div style="width:26px;height:26px;border-radius:50%;background:' + THEME.accent + ';color:white;display:inline-flex;align-items:center;justify-content:center;font-size:0.7em;font-weight:700;">' + (i + 1) + '</div>'
                + (step.icon ? '<div style="margin:6px auto;">' + renderIcon(step.icon, 22) + '</div>' : '')
                + '<div style="font-size:0.72em;font-weight:600;color:' + THEME.textDark + ';margin-top:4px;">' + md(step.title || '') + '</div>'
                + (step.description ? '<div style="font-size:0.58em;color:' + THEME.textMuted + ';margin-top:2px;">' + md(step.description) + '</div>' : '')
                + (step.items ? renderBulletList(step.items) : '')
                + '</div>';
        }

        stepsHtml += '</div>';

        return renderSlideHeader(slide, index)
            + '<div style="padding:4px 20px 20px 20px;">'
            + '<div style="font-size:1.2em;font-weight:700;color:' + THEME.textDark + ';margin-bottom:10px;">' + md(slide.title || '') + '</div>'
            + stepsHtml
            + '</div>'
            + renderSlideFooter(slide)
            + renderNotesBadge(slide);
    }

    function renderQuote(slide, index) {
        const isDark = slide.dark === true;
        const bg = isDark ? THEME.darkNavy : THEME.white;
        const textColor = isDark ? THEME.white : THEME.textDark;
        const mutedColor = isDark ? THEME.lightBlue : THEME.textMuted;

        let inner = '<div style="background:' + bg + ';color:' + textColor + ';height:100%;display:flex;flex-direction:column;justify-content:center;padding:30px 40px;position:relative;">';

        if (!isDark) {
            inner += renderSlideHeader(slide, index);
        }

        inner += '<div style="font-size:4em;line-height:1;color:' + THEME.accent + ';opacity:0.7;">&ldquo;</div>'
            + '<div style="font-size:1.1em;font-style:italic;margin:-10px 0 14px 10px;max-width:90%;">' + md(slide.quote || '') + '</div>'
            + (slide.attribution ? '<div style="font-size:0.75em;font-weight:600;margin-left:10px;">' + md(slide.attribution) + '</div>' : '')
            + (slide.source ? '<div style="font-size:0.6em;color:' + mutedColor + ';margin-left:10px;margin-top:2px;">' + md(slide.source) + '</div>' : '')
            + renderNotesBadge(slide);

        if (!isDark) {
            inner += renderSlideFooter(slide);
        }

        inner += '</div>';
        return inner;
    }

    function renderKeyMetrics(slide, index) {
        const metrics = slide.metrics || [];
        let grid = '<div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:10px;">';

        for (const metric of metrics) {
            let trendHtml = '';
            if (metric.trend) {
                const isUp = metric.trend === 'up';
                const isDown = metric.trend === 'down';
                const arrow = isUp ? '&uarr;' : (isDown ? '&darr;' : '&rarr;');
                const trendColor = isUp ? THEME.success : (isDown ? THEME.warning : THEME.textMuted);
                trendHtml = '<div style="font-size:0.6em;color:' + trendColor + ';margin-top:4px;">'
                    + arrow + ' ' + esc(metric.trend_label || metric.trend)
                    + '</div>';
            }

            const metricColor = metric.color || THEME.accent;
            // Map color names to actual values
            const colorMap = {
                green: THEME.success,
                blue: THEME.primary,
                orange: THEME.warning,
                accent: THEME.accent,
                red: '#DC2626',
            };
            const resolvedColor = colorMap[metricColor] || metricColor;

            grid += '<div style="background:' + THEME.cardBg + ';padding:10px;border-radius:4px;text-align:center;">'
                + '<div style="font-size:1.8em;font-weight:700;color:' + resolvedColor + ';line-height:1;">' + esc(String(metric.value || '')) + '</div>'
                + '<div style="font-size:0.6em;color:' + THEME.textMuted + ';margin-top:4px;">' + esc(metric.label || '') + '</div>'
                + trendHtml
                + '</div>';
        }

        grid += '</div>';

        return renderSlideHeader(slide, index)
            + '<div style="padding:4px 20px 20px 20px;">'
            + '<div style="font-size:1.2em;font-weight:700;color:' + THEME.textDark + ';margin-bottom:10px;">' + md(slide.title || '') + '</div>'
            + grid
            + '</div>'
            + renderSlideFooter(slide)
            + renderNotesBadge(slide);
    }

    function renderChecklist(slide, index) {
        const items = slide.items || [];
        const columns = slide.columns || 1;
        const statusMap = {
            done: { symbol: '&#10003;', color: THEME.success },
            in_progress: { symbol: '&#9679;', color: THEME.accent },
            pending: { symbol: '&#9675;', color: THEME.textLight },
            blocked: { symbol: '&#10007;', color: '#DC2626' },
        };

        let listHtml = '<div style="display:grid;grid-template-columns:repeat(' + columns + ', 1fr);gap:4px 16px;">';
        for (const item of items) {
            const statusInfo = statusMap[item.status] || statusMap.pending;
            listHtml += '<div style="display:flex;align-items:flex-start;gap:6px;padding:3px 0;">'
                + '<span style="color:' + statusInfo.color + ';font-size:0.8em;flex-shrink:0;width:14px;text-align:center;">' + statusInfo.symbol + '</span>'
                + '<div>'
                + '<div style="font-size:0.7em;color:' + THEME.textDark + ';">' + md(item.text || '') + '</div>'
                + (item.note ? '<div style="font-size:0.55em;color:' + THEME.textMuted + ';font-style:italic;">' + md(item.note) + '</div>' : '')
                + '</div>'
                + '</div>';
        }
        listHtml += '</div>';

        return renderSlideHeader(slide, index)
            + '<div style="padding:4px 20px 20px 20px;">'
            + '<div style="font-size:1.2em;font-weight:700;color:' + THEME.textDark + ';margin-bottom:10px;">' + md(slide.title || '') + '</div>'
            + listHtml
            + '</div>'
            + renderSlideFooter(slide)
            + renderNotesBadge(slide);
    }

    function renderImageText(slide, index) {
        const position = slide.image_position || 'left';
        const imageName = slide.image || 'image';
        const content = slide.content || [];

        const imagePlaceholder = '<div style="flex:1;min-width:120px;background:#E2E8F0;border-radius:4px;display:flex;align-items:center;justify-content:center;min-height:120px;color:' + THEME.textMuted + ';font-size:0.65em;text-align:center;padding:10px;">[Image: ' + esc(imageName) + ']</div>';
        const contentHtml = '<div style="flex:1;min-width:120px;">' + renderBulletList(content) + '</div>';

        const leftCol = position === 'left' ? imagePlaceholder : contentHtml;
        const rightCol = position === 'left' ? contentHtml : imagePlaceholder;

        return renderSlideHeader(slide, index)
            + '<div style="padding:4px 20px 20px 20px;">'
            + '<div style="font-size:1.2em;font-weight:700;color:' + THEME.textDark + ';margin-bottom:10px;">' + md(slide.title || '') + '</div>'
            + '<div style="display:flex;gap:14px;align-items:flex-start;">'
            + leftCol
            + rightCol
            + '</div>'
            + '</div>'
            + renderSlideFooter(slide)
            + renderNotesBadge(slide);
    }

    function renderTable(slide, index) {
        const headers = slide.headers || [];
        const rows = slide.rows || [];

        let tableHtml = '<table style="width:100%;border-collapse:collapse;font-size:0.65em;margin-top:6px;">';
        if (headers.length) {
            tableHtml += '<thead><tr>';
            for (const h of headers) {
                tableHtml += '<th style="background:' + THEME.primary + ';color:white;padding:6px 8px;text-align:left;font-weight:600;">' + md(h) + '</th>';
            }
            tableHtml += '</tr></thead>';
        }
        tableHtml += '<tbody>';
        for (let r = 0; r < rows.length; r++) {
            const rowBg = r % 2 === 0 ? THEME.white : THEME.cardBg;
            tableHtml += '<tr>';
            const cells = rows[r] || [];
            for (const cell of cells) {
                tableHtml += '<td style="padding:5px 8px;background:' + rowBg + ';border-bottom:1px solid #E2E8F0;color:' + THEME.textDark + ';">' + md(cell) + '</td>';
            }
            tableHtml += '</tr>';
        }
        tableHtml += '</tbody></table>';

        return renderSlideHeader(slide, index)
            + '<div style="padding:4px 20px 20px 20px;">'
            + '<div style="font-size:1.2em;font-weight:700;color:' + THEME.textDark + ';margin-bottom:6px;">' + md(slide.title || '') + '</div>'
            + tableHtml
            + '</div>'
            + renderSlideFooter(slide)
            + renderNotesBadge(slide);
    }

    function renderContent(slide, index) {
        const content = slide.content || [];
        return renderSlideHeader(slide, index)
            + '<div style="padding:4px 20px 20px 20px;">'
            + '<div style="font-size:1.2em;font-weight:700;color:' + THEME.textDark + ';margin-bottom:10px;">' + md(slide.title || '') + '</div>'
            + renderBulletList(content)
            + '</div>'
            + renderSlideFooter(slide)
            + renderNotesBadge(slide);
    }

    // =============================================
    // Slide renderer dispatch
    // =============================================

    const RENDERERS = {
        title_page: renderTitlePage,
        agenda: renderAgenda,
        stat_cards: renderStatCards,
        definition_cards: renderDefinitionCards,
        content_cards: renderContentCards,
        icon_cards: renderIconCards,
        two_panels: renderTwoPanels,
        comparison: renderComparison,
        section_divider: renderSectionDivider,
        timeline: renderTimeline,
        process: renderProcess,
        quote: renderQuote,
        key_metrics: renderKeyMetrics,
        checklist: renderChecklist,
        image_text: renderImageText,
        table: renderTable,
        content: renderContent,
    };

    function renderSingleSlide(slide, index) {
        const type = slide.type || 'content';
        const renderer = RENDERERS[type] || renderContent;
        return renderer(slide, index);
    }

    // =============================================
    // Navigation and main render
    // =============================================

    function renderSlides(slidesData, meta, theme) {
        slides = slidesData || [];
        metadata = meta || {};
        themeConfig = theme || {};

        if (currentSlideIndex >= slides.length) {
            currentSlideIndex = Math.max(0, slides.length - 1);
        }

        const container = document.getElementById('preview-container');
        if (!container) return;

        if (slides.length === 0) {
            container.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:300px;color:' + THEME.textMuted + ';font-size:1.1em;">No slides to preview. Add slides to your YAML file.</div>';
            return;
        }

        // Build navigator
        let navHtml = '<div class="slide-navigator">';
        navHtml += '<div class="nav-controls">';
        navHtml += '<button class="nav-btn" id="btn-prev" title="Previous slide">&lsaquo;</button>';
        navHtml += '<span class="nav-label">Slide <strong>' + (currentSlideIndex + 1) + '</strong> of ' + slides.length + '</span>';
        navHtml += '<button class="nav-btn" id="btn-next" title="Next slide">&rsaquo;</button>';
        navHtml += '</div>';

        // Thumbnails
        navHtml += '<div class="thumb-strip">';
        for (let i = 0; i < slides.length; i++) {
            const active = i === currentSlideIndex ? ' thumb-active' : '';
            const type = slides[i].type || 'content';
            const label = type.replace(/_/g, ' ');
            navHtml += '<div class="thumb' + active + '" data-index="' + i + '" title="Slide ' + (i + 1) + ': ' + esc(label) + '">';
            navHtml += '<span class="thumb-num">' + (i + 1) + '</span>';
            navHtml += '</div>';
        }
        navHtml += '</div>';
        navHtml += '</div>';

        // Current slide
        const slide = slides[currentSlideIndex];
        const slideType = slide.type || 'content';

        let slideHtml = '<div class="slide-wrapper">';
        slideHtml += '<div class="slide" data-type="' + esc(slideType) + '">';
        slideHtml += '<div>' + renderSingleSlide(slide, currentSlideIndex) + '</div>';
        slideHtml += '</div>';
        slideHtml += '</div>';

        // Slide type label
        slideHtml += '<div class="slide-type-label">Type: ' + esc(slideType) + '</div>';

        container.innerHTML = navHtml + slideHtml;

        // Attach event listeners
        attachNavListeners();
    }

    function attachNavListeners() {
        var btnPrev = document.getElementById('btn-prev');
        var btnNext = document.getElementById('btn-next');

        if (btnPrev) {
            btnPrev.addEventListener('click', function () {
                if (currentSlideIndex > 0) {
                    currentSlideIndex--;
                    renderSlides(slides, metadata, themeConfig);
                }
            });
        }

        if (btnNext) {
            btnNext.addEventListener('click', function () {
                if (currentSlideIndex < slides.length - 1) {
                    currentSlideIndex++;
                    renderSlides(slides, metadata, themeConfig);
                }
            });
        }

        // Thumbnail clicks
        var thumbs = document.querySelectorAll('.thumb');
        thumbs.forEach(function (thumb) {
            thumb.addEventListener('click', function () {
                var idx = parseInt(this.getAttribute('data-index'), 10);
                if (!isNaN(idx) && idx >= 0 && idx < slides.length) {
                    currentSlideIndex = idx;
                    renderSlides(slides, metadata, themeConfig);
                }
            });
        });
    }

    // =============================================
    // Keyboard navigation
    // =============================================

    document.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            if (currentSlideIndex > 0) {
                currentSlideIndex--;
                renderSlides(slides, metadata, themeConfig);
            }
            e.preventDefault();
        } else if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            if (currentSlideIndex < slides.length - 1) {
                currentSlideIndex++;
                renderSlides(slides, metadata, themeConfig);
            }
            e.preventDefault();
        }
    });

    // =============================================
    // Styles injected into the page
    // =============================================

    function injectStyles() {
        var style = document.createElement('style');
        style.textContent = ''
            + '*, *::before, *::after { box-sizing: border-box; }'
            + 'body { margin: 0; padding: 16px; font-family: ' + THEME.font + '; background: #F1F5F9; color: ' + THEME.textDark + '; }'
            + '#preview-container { max-width: 900px; margin: 0 auto; }'
            + '.slide-navigator { margin-bottom: 12px; }'
            + '.nav-controls { display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 8px; }'
            + '.nav-btn { background: ' + THEME.primary + '; color: white; border: none; border-radius: 4px; width: 32px; height: 32px; font-size: 1.3em; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background 0.15s; }'
            + '.nav-btn:hover { background: ' + THEME.darkNavy + '; }'
            + '.nav-label { font-size: 0.85em; color: ' + THEME.textMuted + '; }'
            + '.thumb-strip { display: flex; gap: 4px; overflow-x: auto; padding: 4px 0; }'
            + '.thumb { width: 36px; height: 22px; background: ' + THEME.cardBg + '; border: 2px solid transparent; border-radius: 3px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: border-color 0.15s, background 0.15s; flex-shrink: 0; }'
            + '.thumb:hover { border-color: ' + THEME.lightBlue + '; }'
            + '.thumb-active { border-color: ' + THEME.accent + '; background: white; }'
            + '.thumb-num { font-size: 0.55em; color: ' + THEME.textMuted + '; font-weight: 600; }'
            + '.slide-wrapper { background: white; border-radius: 6px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); overflow: hidden; position: relative; }'
            + '.slide { position: relative; width: 100%; padding-bottom: 56.25%; overflow: hidden; }'
            + '.slide > div { position: absolute; top: 0; left: 0; right: 0; bottom: 0; overflow: auto; }'
            + '.slide-type-label { font-size: 0.7em; color: ' + THEME.textLight + '; margin-top: 6px; text-align: right; }'
            + 'a { color: ' + THEME.accent + '; text-decoration: none; }'
            + 'a:hover { text-decoration: underline; }'
            + '::-webkit-scrollbar { width: 4px; height: 4px; }'
            + '::-webkit-scrollbar-thumb { background: ' + THEME.textLight + '; border-radius: 2px; }';
        document.head.appendChild(style);
    }

    // =============================================
    // Initialize
    // =============================================

    function init() {
        injectStyles();

        // Create container
        var container = document.getElementById('preview-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'preview-container';
            document.body.appendChild(container);
        }

        // Read base64-encoded data from hidden div
        var dataEl = document.getElementById('__data');
        var data = null;
        try {
            if (dataEl && dataEl.textContent) {
                data = JSON.parse(atob(dataEl.textContent.trim()));
            }
        } catch (e) {
            container.innerHTML = '<div style="color:red;padding:20px;">Failed to decode data: ' + String(e) + '</div>';
            return;
        }

        if (data && data.error) {
            container.innerHTML = '<div style="color:red;padding:20px;">' + data.error + '</div>';
            return;
        }
        if (data && data.slides && data.slides.length > 0) {
            try {
                renderSlides(data.slides, data.metadata || {}, data.themeConfig || {});
            } catch (err) {
                container.innerHTML = '<div style="color:red;padding:20px;font-size:0.9em;"><strong>Render error:</strong><br><pre>' + String(err && err.stack ? err.stack : err) + '</pre></div>';
            }
        } else {
            container.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:300px;color:' + THEME.textMuted + ';font-size:0.95em;">No slides found in YAML.</div>';
        }
    }

    // Run initialization when the DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
