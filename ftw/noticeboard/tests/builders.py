from ftw.builder import builder_registry
from ftw.builder.dexterity import DexterityBuilder


class NoticeBoardBuilder(DexterityBuilder):
    portal_type = 'ftw.noticeboard.NoticeBoard'


builder_registry.register('noticeboard', NoticeBoardBuilder)


class NoticeCategoryBuilder(DexterityBuilder):
    portal_type = 'ftw.noticeboard.NoticeCategory'


builder_registry.register('noticecategory', NoticeCategoryBuilder)
