from .views import PostViewset, CommentViewset, LikeViewset
from django.urls import path

urlpatterns = [
    path("", PostViewset.as_view({"get":"list","post":"create"}), name="post-list"),
    path("<int:pk>", PostViewset.as_view({"get":"retrieve","put":"update", "delete":"destroy","patch":"partial_update"}), name="post-detail"),
    path("<int:post_id>/comments/", CommentViewset.as_view({"get":"list","post":"create"}), name="comment-list"),
    path("<int:post_id>/likes/", LikeViewset.as_view({"get":"list","post":"create"}), name="like-list"),
    # path("<int:post_id>/comments/<int:pk>", CommentViewset.as_view({"get":"retrieve","put":"update", "delete":"destroy","patch":"partial_update"})),

]