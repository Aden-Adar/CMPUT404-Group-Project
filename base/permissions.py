from rest_framework import permissions

class IsRemoteNode(permissions.DjangoModelPermissions):

    def has_permission(self, request, view):
        get_accessable_views = ["AllAuthorView", "SingleAuthorView", "FollowerList", "FollowingView", "PostListView", "PostDetailView", "CommentListView", "CommentDetailView", "PostLikesView", "AuthorLikedView", "CommentLikesView"]

        if request.user.groups.filter(name='remote').exists():
            if request.method == "GET" and view.get_view_name() in get_accessable_views:
                return True
            elif request.method == "POST" and view.get_view_name() == "Inbox":
                return True
            else:
                return False
        return True
