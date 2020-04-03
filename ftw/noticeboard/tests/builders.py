from ftw.builder.dexterity import DexterityBuilder
from ftw.builder.registry import builder_registry


class NoticeBuilder(DexterityBuilder):
    portal_type = 'ftw.noticeboard.Notice'


builder_registry.register('ftw.noticeboard.Notice', NoticeBuilder)


class CategoryBuilder(DexterityBuilder):
    portal_type = 'ftw.noticeboard.Category'


builder_registry.register('ftw.noticeboard.Category', CategoryBuilder)
