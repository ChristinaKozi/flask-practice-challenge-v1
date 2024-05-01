from config import app, api
from models import Post, Comment
from flask_restful import Resource
from flask import make_response, jsonify

# create routes here:
class SortedPosts(Resource):
  def get(self):
    posts = Post.query.order_by(Post.title).all()
    posts_dict = [post.to_dict() for post in posts]
    return make_response(posts_dict, 200)

api.add_resource(SortedPosts, '/api/sorted_posts')

class PostsByAuthor(Resource):
  def get(self, author_name):
    capitalized_author_name = author_name.title()
    posts = Post.query.filter(Post.author==capitalized_author_name).all()
    if posts:
      post_dict = [post.to_dict() for post in posts]
      return make_response(post_dict, 200)
    return make_response({'error':'not found'}, 404)

api.add_resource(PostsByAuthor,'/api/posts_by_author/<author_name>')

class PostsByTitle(Resource):
  def get(self, title):
    posts = Post.query.filter(Post.title.contains(title)).all()
    if posts:
      post_dict = [post.to_dict() for post in posts]
      return make_response(post_dict, 200)
    
    return make_response({'error':'not found'}, 404)
    
api.add_resource(PostsByTitle, '/api/search_posts/<title>')

class PostsByComments(Resource):
  def get(self):
    posts = Post.query.all()
    # take in an argument and do something (like the arrow function)
    posts.sort(reverse=True, key=lambda post:len(post.comments))
    return [post.to_dict() for post in posts]

api.add_resource(PostsByComments, '/api/posts_ordered_by_comments')

class MostPopularCommenter(Resource):
  def get(self):
    comments = Comment.query.all()
    if comments:
      names = {}
      for comment in comments:
        if comment.commenter in names:
          names[comment.commenter] += 1
        elif comment.commenter not in names:
          names[comment.commenter] = 1

      most_comments = max(names.values())
      most_popular_commenter = None
      for key, value in names.items():
        if value == most_comments:
          most_popular_commenter = key

      return make_response(jsonify({'commenter': most_popular_commenter}), 200)
    
    return make_response({'error':'not found'}, 404)

api.add_resource(MostPopularCommenter, '/api/most_popular_commenter')

if __name__ == "__main__":
  app.run(port=5555, debug=True)