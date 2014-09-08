/*jslint browser: true, devel: true*/
/*global WebSocket: false, Tipboard: false*/

function updateTileJustLabel(tileId, data, config) {
    var tile = Tipboard.Dashboard.id2node(tileId);
    JustLabel.setDataByKeys(tileId, data, 'all');
    var highlighterNode = $('#' + tileId + '-just-label').parent();
    Tipboard.DisplayUtils.applyHighlighterConfig(
        highlighterNode, config['just-label-color'], config.fading_background
    );
    Tipboard.TileDisplayDecorator.runAllDecorators(tile);
}

Tipboard.Dashboard.registerUpdateFunction('just_label', updateTileJustLabel);

JustLabel = {
    setDataByKeys: function(tileId, data, keys) {
        Tipboard.Dashboard.setDataByKeys(tileId, data, keys);
    },
    setJustLabelColor: function(tileId, meta) {
        // DEPRECATED function, Tipboard.DisplayUtils.applyHighlighterConfig
        var color = meta['just-label-color'];
        if (color !== void 0) {
            color = Tipboard.DisplayUtils.replaceFromPalette(color);
            var dst = $('#' + tileId + '-just-label').parent();
            $(dst).css('background-color', color);
        }
    }
};
