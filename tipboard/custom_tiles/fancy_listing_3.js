/*jslint browser: true, devel: true*/
/*global WebSocket: false, Tipboard: false*/

function updateTileFancyListing3(tileId, data, config, tipboard) {
    var tile = Tipboard.Dashboard.id2node(tileId);
    var nodeToClone = FancyListing3.initContainer(tile);
    if (nodeToClone === void 0) {
        return false;
    }
    FancyListing3.populateItems(tile, nodeToClone, data);
    FancyListing3.applyConfig(tile, config);
    Tipboard.TileDisplayDecorator.runAllDecorators(tile);
    if (config['vertical_center'] === true) {
        FancyListing3.verticalCenter(tile);
    }
}

Tipboard.Dashboard.registerUpdateFunction('fancy_listing_3', updateTileFancyListing3);

FancyListing3 = {
    initContainer: function(tile) {
        var nodeToClone = $(tile).find('.fancy-listing-3-item')[0];
        if (nodeToClone === void 0) {
            console.log('ABORTING - no node to clone');
            return false;
        }
        $(tile).find('.fancy-listing-3-item').slice(1).remove();
        return nodeToClone;
    },
    appendCloned: function(tile, nodeToClone) {
        var container = $(tile).find('.tile-content')[0];
        $(nodeToClone).clone().appendTo(container);
    },
    populateItems: function(tile, clonedNode, data) {
        $.each(data, function(idx, tileData) {
            FancyListing3.appendCloned(tile, clonedNode);
            FancyListing3.replaceData(tile, tileData);
        });
    },
    applyConfig: function(tile, config) {
        $.each(config, function(idx, tileConfig) {
            if (/\d+/.test(idx)) {
                var item = $(tile).find('.fancy-listing-3-item')[idx];
                // set color
                var color = Tipboard.DisplayUtils.replaceFromPalette(
                    tileConfig['label_color']
                );
                $(item).find('.fancy-listing-3-label').css('background-color', color);
                // set centering
                if (tileConfig['center'] === true) {
                    $(item).find('.fancy-listing-3-def').css(
                        'text-align', 'center'
                    );
                }
            }
        });
    },
    verticalCenter: function(tile) {
        // TODO: replace it with css class and toggle the class
        containerHeight = $(tile).find('.tile-content').height();
        children = $(tile).find('.tile-content').children().slice(1);
        var childrensHeight = 0;
        $.each(children, function(idx, child) {
            childrensHeight += $(child).outerHeight(true);
        });
        positionToSet = (containerHeight - childrensHeight) / 2;
        if (positionToSet > 0) {
            $(children[0]).css('padding-top', positionToSet);
        }
    },
    replaceData: function(tile, tileData) {
        var lastItem = $(tile).find('.fancy-listing-3-item:last-child')[0];
        $(lastItem).find('.fancy-listing-3-label-inside').html(tileData['label']);
        $(lastItem).find('.fancy-listing-3-term').html(tileData['text']);
        $(lastItem).find('.fancy-listing-3-desc').html(tileData['description']);
    }
};

