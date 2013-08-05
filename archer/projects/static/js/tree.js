function collapse(that, children, speed) {
    if (speed == undefined)
        children.hide('fast');
    else
        children.hide();
    $(that).attr('title', 'Expand this branch').find(' > i').addClass('icon-folder-close').removeClass('icon-folder-open');
}

function expand(that, children) {
    children.show('fast');
    $(that).attr('title', 'Collapse this branch').find(' > i').addClass('icon-folder-open').removeClass('icon-folder-close');
}
$(function () {
    $('.tree li:has(ul)').addClass('parent_li').find(' > span.folder > span.name').attr('title', 'Collapse this branch');
    $('.tree li.parent_li > span.folder').on('click', function (e) {
        var children = $(this).parent('li.parent_li').find(' > ul > li');
        var that = $(this).find(' > span.name');
        if (children.is(":visible")) {
            collapse(that, children);
        } else {
            expand(that, children);
        }
        e.stopPropagation();
    });
    $('.tree a.collapse_all').on('click', function (e) {
        $('.tree li.parent_li > ul > li').hide();
        $('.tree li.parent_li > span.folder > span.name').attr('title', 'Expand this branch').find(' > i').addClass('icon-folder-close').removeClass('icon-folder-open');
        ;
    });
    $('.tree a.expand_all').on('click', function (e) {
        $('.tree li.parent_li > ul > li').show();
        $('.tree li.parent_li > span.folder > span.name').attr('title', 'Collapse this branch').find(' > i').addClass('icon-folder-open').removeClass('icon-folder-close');
    });

    $('.tree li.parent_li > span.folder > span.actions').on('click', function (e) {
        e.stopPropagation();
    });
    $('.tree li.parent_li > ul > li').hide();
    $('.tree').show();
});