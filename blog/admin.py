from django.contrib import admin


from .models import Admin_Blog, Category_Blog, Tag_Blog, Site_Blog, Post_Blog, Comment_Blog, Like_Blog, Follower_Blog, Note_Blog, Partage_Blog, Infos_Blog

class AdminBlogAdmin(admin.ModelAdmin):
    list_display = ('email', 'grade')
    search_fields = ('email',)

class CategoryBlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

class TagBlogAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class SiteBlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'id_sitepam', 'id_Admin_Blog', 'Couleur', 'created_at', 'updated_at')
    search_fields = ('title', 'id_sitepam__nom_site', 'id_Admin_Blog__email')
    list_filter = ('created_at', 'updated_at')

class PostBlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'author__email')
    list_filter = ('created_at', 'updated_at')

class CommentBlogAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'updated_at')
    search_fields = ('post__title', 'author__email')
    list_filter = ('created_at', 'updated_at')

class LikeBlogAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('post__title', 'user__email')
    list_filter = ('created_at',)

class FollowerBlogAdmin(admin.ModelAdmin):
    list_display = ('site', 'user_Standard', 'user_livreur', 'user_main', 'created_at')
    search_fields = ('site__title', 'user_Standard__email', 'user_livreur__email', 'user_main__email')
    list_filter = ('created_at',)

class NoteBlogAdmin(admin.ModelAdmin):
    list_display = ('site', 'user_Standard', 'user_livreur', 'valeur', 'created_at')
    search_fields = ('site__title', 'user_Standard__email', 'user_livreur__email', 'valeur')
    list_filter = ('created_at',)

class PartageBlogAdmin(admin.ModelAdmin):
    list_display = ('data_post', 'data_site', 'user_Standard', 'user_livreur', 'user_main', 'created_at')
    search_fields = ('data_post__title', 'data_site__Domaine', 'user_Standard__email', 'user_livreur__email', 'user_main__email')
    list_filter = ('created_at',)

class InfosBlogAdmin(admin.ModelAdmin):
    list_display = ('site', 'phone1', 'phone2', 'adresse', 'about', 'Bio', 'Infos_supplementaires')
    search_fields = ('site__title', 'phone1', 'phone2', 'adresse', 'about', 'Bio', 'Infos_supplementaires')

admin.site.register(Admin_Blog, AdminBlogAdmin)
admin.site.register(Category_Blog, CategoryBlogAdmin)
admin.site.register(Tag_Blog, TagBlogAdmin)
admin.site.register(Site_Blog, SiteBlogAdmin)
admin.site.register(Post_Blog, PostBlogAdmin)
admin.site.register(Comment_Blog, CommentBlogAdmin)
admin.site.register(Like_Blog, LikeBlogAdmin)
admin.site.register(Follower_Blog, FollowerBlogAdmin)
admin.site.register(Note_Blog, NoteBlogAdmin)
admin.site.register(Partage_Blog, PartageBlogAdmin)
admin.site.register(Infos_Blog, InfosBlogAdmin)


# Register your models here.
