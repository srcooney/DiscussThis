import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
import json

import logging

import re
from google.appengine.api import images
from google.appengine.ext import blobstore

from google.appengine.api import files
import urllib
import time
# from PythonMagick import Image
# import PythonMagick

# import wand





HEAD = """
<script src="javascript/jquery-2.1.1.min.js"></script>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css">

<!-- Optional theme-->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap-theme.min.css">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.0/js/bootstrap.min.js"></script>

<script src="javascript/make_header_active.js"></script>



<link type="text/css" rel="stylesheet" href="css/fixed_location.css" />

"""
# <script src="javascript/comment_button_click.js"></script>

ALL_PAGE_HEADER ="""

    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/ManagePage">DiscussIt</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="/ManagePage">Manage My Account</a></li>
            <li><a href="/ViewAllDocumentsPage">View All Documents</a></li>
            <li><a href="/CreateDocumentPage">Create A New Document</a></li>
            <li><a href="/SearchDocumentsPage">Search For A Document</a></li>
            <li><a href="%s">Sign out</a></li>
              </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    

"""

VIEWADOCUMENT_PAGE_HEADER ="""

    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/ManagePage">DiscussIt</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="/ManagePage">Manage My Account</a></li>
            <li><a href="/ViewAllDocumentsPage">View All Documents</a></li>
            <li><a href="/CreateDocumentPage">Create A New Document</a></li>
            <li><a href="/SearchDocumentsPage">Search For A Document</a></li>
            <li class="dropdown">
                <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="true">follow<span class="caret"></span></a>
                <ul class="dropdown-menu" role="menu">
                  <li><a href="/AddDocumentFollowerFromAuthorService?documentName=%s&author=%s">%s</a></li>
                  <li><a href="/AddDocumentFollowerService?documentName=%s">%s</a></li>
                </ul>
              </li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    

"""

CREATE_PAGE = """
    <form action="/CreateDocumentService" method="post">
        <br><br><br>
          <h4>Name Your Document</h4>
          <textarea name="documentName" class="form-control" rows="1" cols="30" width="10%"></textarea>
          <input type="submit" class="btn btn-default" value="Create Document!">
    </form>
"""

COMMENT_BUTTON_CLICK_SCRIPT = """

<script>
var count = %d;
$(document).ready(function () {
    $("#CommentButton").click(function(){
        $("[id=commentBlock]").remove()
        $(".point").remove()
        $("[id=images]").click(function(e){
           var parentOffset = $(this).parent().offset(); 
           var relX = e.pageX - parentOffset.left;
           var relY = e.pageY - parentOffset.top;
           var form = '<form id="commentBlock" action="/AddCommentService?documentName=%s" method="post"> \
            <p class="fixedLocationTitleLabel">Title</p> \
             <textarea rows="1" cols="40" wrap="soft" style="width:20%%" type="text" class="form-control fixedLocationTitleTextBox" name="titleString"/> \
           <textarea rows="5" cols="40" wrap="soft" style="width:20%%" type="text" class="form-control fixedLocationComment" name="commentString"/> \
               <input type="hidden" name="relX" value="' +relX+ '"/> <input type="hidden" name="relY" value="' +relY+ '"/> \
               <input type="hidden" name="symbol" value="C' +count+ '"/>\
           <div><input type="submit" class="btn btn-default fixedLocationCommentConfirm" value="Confirm Comment"></div>  \
           </form>'
            var commentPoint = '<input class="btn btn-success btn-xs point" type="submit" id="C' +count+'"'+ 'value="C'+count+'"/>';
            $("body").append(form,commentPoint);         // Append the new elements 
            $("#C" +count).css({ 'position': 'absolute','left':relX, 'top':relY , 'opacity':0.5});
            $("[id=images]").off();
        });
    });
});
</script>
"""

ERROR_BUTTON_CLICK_SCRIPT = """

<script>
var counte = %d;
$(document).ready(function () {
    $("#ErrorButton").click(function(){
        $("[id=commentBlock]").remove()
        $(".point").remove()
        $("[id=images]").click(function(e){
           var parentOffset = $(this).parent().offset(); 
           var relX = e.pageX - parentOffset.left;
           var relY = e.pageY - parentOffset.top;
           var form = '<form id="commentBlock" action="/AddCommentService?documentName=%s" method="post"> \
           <p class="fixedLocationTitleLabel">Title</p> \
             <textarea rows="1" cols="40" wrap="soft" style="width:20%%" type="text" class="form-control fixedLocationTitleTextBox" name="titleString"/> \
           <textarea rows="5" cols="40" wrap="soft" style="width:20%%" type="text" class="form-control fixedLocationComment" name="commentString"/>\
               <input type="hidden" name="relX" value="' +relX+ '"/> <input type="hidden" name="relY" value="' +relY+ '"/> \
               <input type="hidden" name="symbol" value="E' +counte+ '"/>\
           <div><input type="submit" class="btn btn-default fixedLocationCommentConfirm" value="Confirm Comment"></div>  \
           </form>'
            var errorPoint = '<input class="btn btn-danger btn-xs point" type="submit" id="E' +counte+'"'+ 'value="E'+counte+'"/>';
            $("body").append(form,errorPoint);         // Append the new elements 
            $("#E" +counte).css({ 'position': 'absolute','left':relX, 'top':relY , 'opacity':0.5});
            $("[id=images]").off();
        });
    });
});
</script>
"""

DISPLAY_COMMENT_BUTTONS_SCRIPT = """

<script>

$(document).ready(function () {
    jsonObj = JSON.parse('%s')
    var documentName='%s'
    for ( var i = 0; i < jsonObj.commentSymbol.length; i++ ) {
    (function(i) {
        $('#' + jsonObj.commentSymbol[i] + '').click(function(){
                $("[id=commentBlock]").remove()
                $(".point").remove()
                var comment = '<textarea id="commentBlock" class="form-control fixedLocationComment" style="width:20%%"\
                rows="5" cols="40" wrap="soft" readonly>' + jsonObj.commentList[i] + '</textarea>';
                
                var upvote = '<form id="commentBlock" action="/UpVoteCommentService" method="post"> \
                <input type="hidden" name="commentSymbol" value="' + jsonObj.commentSymbol[i] +'"/> \
                <input type="hidden" name="documentName" value="' + documentName +'"/> \
                <input class="btn-info btn-xs fixedLocationCommentBannerUpvote" type=submit value="^"></form>';
                
                var downvote = '<form id="commentBlock" action="/DownVoteCommentService" method="post"> \
                <input type="hidden" name="commentSymbol" value="' + jsonObj.commentSymbol[i] +'"/> \
                <input type="hidden" name="documentName" value="' + documentName +'"/> \
                <input class="btn-info btn-xs fixedLocationCommentBannerDownvote" type=submit value="v"></form>';
                
                var votes = '<form id="commentBlock" action="/" method="get"> \
                <input class="btn-info btn-lg fixedLocationCommentBannerVotes" type=submit value="' + jsonObj.commentVote[i] + '"></form>';
                
                var deleteb = '<form id="commentBlock" action="/DeleteCommentService" method="post"> \
                <input type="hidden" name="commentSymbol" value="' + jsonObj.commentSymbol[i] +'"/> \
                <input type="hidden" name="documentName" value="' + documentName +'"/> \
                <input class="btn-info btn-lg fixedLocationCommentBannerDelete" type=submit value="delete"></form>';
                var comment2 = '<form id="commentBlock" action="/AddCommentOnCommentService" method="post"> \
                <input class="btn-info btn-lg fixedLocationCommentBannerComment" type=submit value="Comment"> \
                <input type="hidden" name="commentSymbol" value="' + jsonObj.commentSymbol[i] +'"/> \
                <input type="hidden" name="documentName" value="' + documentName +'"/> \
                <input name="newComment" style="width:20%%" class="form-control fixedLocationCommentBannerCommentText" type=text placeholder="Let Your Voice Be Heard."></form>';
                
                if(jsonObj.commentOnCommentList[jsonObj.commentSymbol[i]] != null){
                    for ( var j = 0; j < jsonObj.commentOnCommentList[jsonObj.commentSymbol[i]].length; j++ ) {
                        (function(j) {
                            var height = 360 + j*60;
                            var textarea = '<textarea id="commentBlock" class="form-control fixedLocationCommentBannerCommentText" style="width:20%%;top:'+height+ '" >'  \
                             +jsonObj.commentOnCommentList[jsonObj.commentSymbol[i]][j] + '</textarea>';
                             $("body").append(textarea);
                        }   
                        )(j);
                     
                    }
                }
                
                $("body").append(comment,downvote,upvote,votes,deleteb,comment2);
                
        });
        }   
        )(i);   
    } 
    
    
    
        for ( var i = 0; i < jsonObj.commentSymbol.length; i++ ) {
        (function(i) {
        $('#' + jsonObj.commentSymbol[i] + '').tooltip(function(){
                
        });
        }   
        )(i);   
    }
    
    
});

</script>


"""

DISPLAY_ERROR_BUTTONS_SCRIPT = """

<script>

$(document).ready(function () {
    jsonObjE = JSON.parse('%s')
    var documentName='%s'
    for ( var i = 0; i < jsonObjE.commentSymbol.length; i++ ) {
    (function(i) {
    
        $('#' + jsonObjE.commentSymbol[i] + '').click(function(){
                $("[id=commentBlock]").remove()
                $(".point").remove()
                var comment = '<textarea id="commentBlock" class="form-control fixedLocationComment" style="width:20%%"\
                rows="5" cols="40" wrap="soft" readonly>' + jsonObjE.commentList[i] + '</textarea>';
                
                var upvote = '<form id="commentBlock" action="/UpVoteCommentService" method="post"> \
                <input type="hidden" name="commentSymbol" value="' + jsonObjE.commentSymbol[i] +'"/> \
                <input type="hidden" name="documentName" value="' + documentName +'"/> \
                <input class="btn-info btn-xs fixedLocationCommentBannerUpvote" type=submit value="^"></form>';
                
                var downvote = '<form id="commentBlock" action="/DownVoteCommentService" method="post"> \
                <input type="hidden" name="commentSymbol" value="' + jsonObjE.commentSymbol[i] +'"/> \
                <input type="hidden" name="documentName" value="' + documentName +'"/> \
                <input class="btn-info btn-xs fixedLocationCommentBannerDownvote" type=submit value="v"></form>';
                
                var votes = '<form id="commentBlock" action="/" method="get"> \
                <input class="btn-info btn-lg fixedLocationCommentBannerVotes" type=submit value="' + jsonObjE.commentVote[i] + '"></form>';
                
                var deleteb = '<form id="commentBlock" action="/DeleteCommentService" method="post"> \
                <input type="hidden" name="commentSymbol" value="' + jsonObjE.commentSymbol[i] +'"/> \
                <input type="hidden" name="documentName" value="' + documentName +'"/> \
                <input class="btn-info btn-lg fixedLocationCommentBannerDelete" type=submit value="delete"></form>';
                var comment2 = '<form id="commentBlock" action="/AddCommentOnCommentService" method="post"> \
                <input class="btn-info btn-lg fixedLocationCommentBannerComment" type=submit value="Comment"> \
                <input type="hidden" name="commentSymbol" value="' + jsonObjE.commentSymbol[i] +'"/> \
                <input type="hidden" name="documentName" value="' + documentName +'"/> \
                <input name="newComment" style="width:20%%" class="form-control fixedLocationCommentBannerCommentText" type=text placeholder="Let Your Voice Be Heard."></form>';
                
                if(jsonObjE.commentOnCommentList[jsonObjE.commentSymbol[i]] != null){
                    for ( var j = 0; j < jsonObjE.commentOnCommentList[jsonObjE.commentSymbol[i]].length; j++ ) {
                        (function(j) {
                            var height = 360 + j*60;
                            var textarea = '<textarea id="commentBlock" class="form-control fixedLocationCommentBannerCommentText" style="width:20%%;top:'+height+ '" >'  \
                             +jsonObjE.commentOnCommentList[jsonObjE.commentSymbol[i]][j] + '</textarea>';
                             $("body").append(textarea);
                        }   
                        )(j);
                     
                    }
                }
                
                $("body").append(comment,downvote,upvote,votes,deleteb,comment2);
                
        });
        }   
        )(i);   
    }
    
    
    
    for ( var i = 0; i < jsonObjE.commentSymbol.length; i++ ) {
        (function(i) {
        $('#' + jsonObjE.commentSymbol[i] + '').tooltip(function(){
                
        });
        }   
        )(i);   
    } 
});

</script>


"""




ALL_STREAMS_NAME = 'all_streams'
def stream_key(streamName=ALL_STREAMS_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Stream', streamName)


ALL_DOCUMENTS_NAME = 'all_writings'
def document_key(documentName=ALL_DOCUMENTS_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Document', documentName)

class CommentOnComments(ndb.Model):
    comments = ndb.StringProperty(repeated=True) # E.g., 'home', 'work'

class Document(ndb.Model):
    documentName = ndb.StringProperty()
    owner = ndb.StringProperty()
    author = ndb.StringProperty()
    followers = ndb.StringProperty(repeated=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    count = ndb.IntegerProperty()
    imageList = ndb.StringProperty(repeated=True)


    commentList = ndb.StringProperty(repeated=True)
    commentVote = ndb.IntegerProperty(repeated=True)
    commentX = ndb.StringProperty(repeated=True)
    commentY = ndb.StringProperty(repeated=True)
    commentSymbol = ndb.StringProperty(repeated=True)
    commentOnCommentsList = ndb.JsonProperty()
    commentCount = ndb.IntegerProperty()
    commentTitle = ndb.StringProperty(repeated=True)
    
    errorList = ndb.StringProperty(repeated=True)
    errorVote = ndb.IntegerProperty(repeated=True)
    errorX = ndb.StringProperty(repeated=True)
    errorY = ndb.StringProperty(repeated=True)
    errorSymbol = ndb.StringProperty(repeated=True)
    errorCommentOnCommentsList = ndb.JsonProperty()
    errorCount = ndb.IntegerProperty()
    errorTitle = ndb.StringProperty(repeated=True)
    
class LoginPage(webapp2.RequestHandler):         
    def get(self):
        user = users.get_current_user()

        if user:
            self.redirect("/ManagePage")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class ManagePage(webapp2.RequestHandler):         
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
            return
        self.response.write("""<html>""")
        self.response.write(HEAD)
        self.response.write("""<body style="background-color:#D3D3CB">""")
        self.response.write(ALL_PAGE_HEADER % users.create_logout_url("/"))
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        self.response.out.write("""<br><br><br><h1>My Documents</h1>""")
        
        
        foundOwner = False
        for document in documents:
            if document.owner == users.get_current_user().email():
                if(not foundOwner):
                    self.response.out.write("""<div class ="row"><div class="col-md-6"><table class ="table"><thead><tr><th>Author</th>
                    <th>Title</th><th># Comments</th><th># Errors</th><th>Number of Views</th><th><p>Delete</th></tr></thead>""")
                foundOwner = True
                self.response.out.write("""<tr>""")
                self.response.out.write("""<td><p>%s</p>
                                               </td>""" %(document.author))
                self.response.out.write("""<td><form action="/IncreaseDocumentCountService?documentName=%s" method="post">
                                                <a href="#" onclick="this.parentNode.submit()">
                                                  <p align="center">%s</p></a></form>
                                               </td>""" %(document.documentName,document.documentName))
                self.response.out.write("""<td><p>%s</p></td>""" % (len(document.commentList)))
                self.response.out.write("""<td><p>%s</p></td>""" % (len(document.errorList)))
                self.response.out.write("""<td><p>%d</p></td>""" % (document.count))
                self.response.out.write("""<td><form action="/DeleteDocumentService?documentName=%s" method="post">
                <input type="submit" class="btn btn-default" value="delete"></form></td>""" % document.documentName)
                self.response.out.write("""</tr>""")
        
          
        self.response.out.write("""</table></div></div>""")  
        if(not foundOwner):
            self.response.out.write("""<h4>You have not uploaded any documents. Please click create Document above to start.</h4>""")      
        self.response.out.write("""<h1>Following</h1>""")
        
        
        foundFollower = False
        for document in documents:
            for follower in document.followers:
                if follower == users.get_current_user().email():
                    if(not foundFollower):
                        self.response.out.write("""<div class ="row"><div class="col-md-6"><table class ="table"><thead><tr><th>Author</th>
                        <th>Title</th><th># Comments</th><th># Errors</th><th>Number of Views</th><th><p>Delete</th></tr></thead>""")
                    foundFollower = True
                    self.response.out.write("""<tr>""")
                    self.response.out.write("""<td><p>%s</p>
                                                   </td>""" %(document.author))
                    self.response.out.write("""<td><form action="/IncreaseDocumentCountService?documentName=%s" method="post">
                                                    <a href="#" onclick="this.parentNode.submit()">
                                                      <p align="center">%s</p></a></form>
                                                   </td>""" %(document.documentName,document.documentName))
                    self.response.out.write("""<td><p>%s</p></td>""" % (len(document.commentList)))
                    self.response.out.write("""<td><p>%s</p></td>""" % (len(document.errorList)))
                    self.response.out.write("""<td><p>%d</p></td>""" % (document.count))
                    self.response.out.write("""<td><form action="/UnFollowDocumentService?documentName=%s" method="post">
                    <input type="submit" class="btn btn-default" value="Unfollow"></form></td>""" % document.documentName)
                    self.response.out.write("""</tr>""")

        
        self.response.out.write("""</table></div></div>""") 
        if(not foundFollower):
            self.response.out.write("""<h4>You have not followed any documents.</h4>""") 
        self.response.write("""</body>""")
        self.response.write("""</html>""")
        
        
        
class ViewADocumentPage(webapp2.RequestHandler):         
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
            return
        documentName = self.request.get('documentName')
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        for document in documents:
            if document.documentName == documentName:
                break
            
            
            
        self.response.write("""<html><head>""")
        self.response.write(HEAD)
        self.response.write(COMMENT_BUTTON_CLICK_SCRIPT % (document.commentCount,documentName))
        self.response.write(ERROR_BUTTON_CLICK_SCRIPT % (document.errorCount,documentName))
        
        self.response.write("""</head><body style="background-color:#D3D3CB">""")
        self.response.write(VIEWADOCUMENT_PAGE_HEADER % (document.documentName,document.author,document.author, document.documentName,document.documentName))
        if(len(document.imageList) == 0):
            self.response.write("""
                <form  action="/CreateDocumentPage" method="get">
                <input type="hidden" name="documentName" value="%s"/>
                <input class="btn-info btn-lg fixedLocationAddPages" type=submit value="Add files to your document"></form>
            """ % documentName)
        else:
            self.response.write("""
            <input id="CommentButton" class="fixedLocationCommentButton btn btn-default" type="button" value="Add Comment" />
            <input style="width:115" id="ErrorButton" class="fixedLocationErrorButtton btn btn-default" type="button" value="Add Error"/>
            </br></br></br>
            """)
            for image in document.imageList:
                self.response.write("""
                <img id="images" src="%s" style="margin-left:170px;">
                
                """ % image) 
            
            for i in range(len(document.commentList)):
                self.response.write("""
                    <input title ="%s" class="btn btn-success btn-xs" type="submit" id="%s" class="fixedLocationP" value="%s" style="position: absolute; left: %spx; top: %spx; opacity: 0.5;">
                """ % (document.commentList[i],document.commentSymbol[i],document.commentTitle[i],document.commentX[i],document.commentY[i]))
            
            for i in range(len(document.errorList)):
                self.response.write("""
                    <input title ="%s" class="btn btn-danger btn-xs" type="submit" id="%s" class="fixedLocationP" value="%s" style="position: absolute; left: %spx; top: %spx; opacity: 0.5;">
                """ % (document.errorList[i],document.errorSymbol[i],document.errorTitle[i],document.errorX[i],document.errorY[i]))
            
            jsonObj = json.dumps({"commentVote":document.commentVote,"commentSymbol":document.commentSymbol,"commentList":document.commentList,"commentOnCommentList":document.commentOnCommentsList})
            self.response.write(DISPLAY_COMMENT_BUTTONS_SCRIPT % (jsonObj,documentName))
            
            jsonObjE = json.dumps({"commentVote":document.errorVote,"commentSymbol":document.errorSymbol,"commentList":document.errorList,"commentOnCommentList":document.errorCommentOnCommentsList})
            self.response.write(DISPLAY_ERROR_BUTTONS_SCRIPT % (jsonObjE,documentName))
        
        self.response.write("""</body>""")
        self.response.write("""</html>""")


class SearchDocumentsPage(webapp2.RequestHandler):         
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
            return
        searchName = self.request.get('searchName')
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        self.response.write("""<html><head>""")
        self.response.write(HEAD)
        self.response.write("""</head><body style="background-color:#D3D3CB">""")
        self.response.write(ALL_PAGE_HEADER % users.create_logout_url("/"))
        self.response.out.write("""
            <form action="/SearchDocumentService" method="post">
            <br><br><br>
              <h4>Search For A Document</h4>
              <textarea style="width:20%%" name="searchName" class="form-control" rows="1" cols="30"></textarea>
              <br>
              <input class="btn btn-success" type="submit" value="Search">
            </form>
            
            """)
        
        if(searchName == "none"):
            self.response.out.write("""
                <h4>0 results were found</h4>
            """)
        elif(searchName != ""):
            self.response.out.write("""<div class ="row"><div class="col-md-6"><table class ="table">""")
            self.response.out.write("""<tr>""")
            i = 0
            for document in documents:
                
                if((i % 5) == 0):
                    self.response.out.write("""</tr>""")
                    self.response.out.write("""<tr>""")
                if(document.documentName == searchName):
                    
                    if(len(document.imageList) == 0):
                        self.response.out.write("""<td><form action="/IncreaseDocumentCountService?documentName=%s" method="post">
                                                    <a href="#" onclick="this.parentNode.submit()">
                                                      <p align="center">%s</p>
                                                      <img width="200" height="200" src="%s">
                                                      </a></form>
                                                   </td>""" %(document.documentName,document.documentName,"http://epaper2.mid-day.com/images/no_image_thumb.gif"))
                    else:
                        self.response.out.write("""<td><form action="/IncreaseDocumentCountService?documentName=%s" method="post">
                                                    <a href="#" onclick="this.parentNode.submit()">
                                                      <p align="center">%s</p>
                                                      <img width="200" height="200" src="%s">
                                                      </a></form>
                                                   </td>""" %(document.documentName,document.documentName,document.imageList[0]))
                    i+=1
            

        self.response.write("""</body>""")
        self.response.write("""</html>""")        
        
class ViewAllDocumentsPage(webapp2.RequestHandler):         
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
            return
        documentName = self.request.get('documentName')
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        self.response.write("""<html><head>""")
        self.response.write(HEAD)
        self.response.write("""</head><body style="background-color:#D3D3CB">""")
        self.response.write(ALL_PAGE_HEADER % users.create_logout_url("/"))
        self.response.out.write("""<br><br><br><h1>View All Documents</h1>""")
        self.response.out.write("""<div class ="row"><div class="col-md-6"><table class ="table">""")
        self.response.out.write("""<tr>""")
        i = 0
        for document in documents:
            
            if((i % 5) == 0):
                self.response.out.write("""</tr>""")
                self.response.out.write("""<tr>""")
            if(len(document.imageList) == 0):
                self.response.out.write("""<td><form action="/IncreaseDocumentCountService?documentName=%s" method="post">
                                            <a href="#" onclick="this.parentNode.submit()">
                                              <p align="center">%s</p>
                                              <img width="200" height="200" src="%s">
                                              </a></form>
                                           </td>""" %(document.documentName,document.documentName,"http://epaper2.mid-day.com/images/no_image_thumb.gif"))
            else:
                self.response.out.write("""<td><form action="/IncreaseDocumentCountService?documentName=%s" method="post">
                                            <a href="#" onclick="this.parentNode.submit()">
                                              <p align="center">%s</p>
                                              <img width="200" height="200" src="%s">
                                              </a></form>
                                           </td>""" %(document.documentName,document.documentName,document.imageList[0]))
            i+=1
            
            
#         self.response.out.write("""</tr>""")

        self.response.write("""</body>""")
        self.response.write("""</html>""")

class CreateDocumentPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
            return
        documentName = self.request.get('documentName')
        author = self.request.get('author')
        self.response.write("""<html>""")
        self.response.write(HEAD)
        self.response.write("""<body style="background-color:#D3D3CB">""")
        self.response.write(ALL_PAGE_HEADER % users.create_logout_url("/"))
        
        
        
        if(documentName == "" or author == "none" or documentName == "none" ):
            if(author == "none"):
                self.response.out.write("""
                <form action="/CreateDocumentService" method="post">
                <br><br><br>
                  <h4>Author</h4>
                  <textarea style="width:20%%" name="author" class="form-control" rows="1" cols="30"></textarea>
                  <p style="color:red">Please Enter an Author Name</p>
                  """)
            else:
                self.response.out.write("""
                <form action="/CreateDocumentService" method="post">
                <br><br><br>
                  <h4>Author</h4>
                  <textarea style="width:20%%" name="author" class="form-control" rows="1" cols="30">%s</textarea>
                  """ % (author))
                
            if(documentName == "none"):
                self.response.out.write("""
                  <h4>Title</h4><textarea style="width:20%%" name="documentName" class="form-control" rows="1" cols="30"></textarea>
                  <p style="color:red">Please Enter an Document Title</p>
                  <br>
                  <input class="btn btn-success" type="submit" value="Choose Name">
                </form>
                
                """)
            else:
                self.response.out.write("""
                  <h4>Title</h4><textarea style="width:20%%" name="documentName" class="form-control" rows="1" cols="30">%s</textarea>
                  <br>
                  <input class="btn btn-success" type="submit" value="Choose Name">
                </form>
                
                """ %(documentName))
        else:
            self.response.out.write("""
            <br><br><br>
            <h2>%s</h2>
              <h4>Add files to your document</h4>

            
            """ % documentName)
            self.response.write(GOOD_UPLOADER_FIRST)
            self.response.write("""<input type="hidden" name="documentName" value="%s">""" % documentName)
            self.response.write(GOOD_UPLOADER_SECOND)
        
        self.response.write("""</body>""")
        self.response.write("""</html>""")        
class IncreaseDocumentCountService(webapp2.RequestHandler): 
    def post(self):
        
        documentName = self.request.get('documentName')
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        for document in documents:
            if document.documentName == documentName:
                break
        
        document.count +=1

        document.put()
        
        self.redirect('/ViewADocumentPage?documentName=%s' % (documentName))

class CreateDocumentService(webapp2.RequestHandler): 
    def post(self):
        document = Document(parent=document_key(ALL_DOCUMENTS_NAME))
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        documentName = self.request.get('documentName')
        author = self.request.get('author')
        if(documentName != "" and author != "" and documentName != "none" and author != "none"):
            document.documentName = self.request.get('documentName')
            document.author = self.request.get('author')
            document.owner = users.get_current_user().email()
            document.count = 0
            document.commentCount = 0
            document.errorCount = 0
            document.commentOnCommentsList = {}
            document.errorCommentOnCommentsList = {}
            document.put()
        
        if(documentName == ""):
            documentName = "none"
        if(author == ""):
            author = "none"
        self.redirect('/CreateDocumentPage?documentName=%s&author=%s' %(documentName,author))
        
class SearchDocumentService(webapp2.RequestHandler): 
    def post(self):
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        searchName = self.request.get('searchName')
        found = False
        for document in documents:
            if document.documentName == searchName:
                found = True
                break
        if(found):
            self.redirect('/SearchDocumentsPage?searchName=' +document.documentName)
        else:
            self.redirect('/SearchDocumentsPage?searchName=' +"none")
            
class AddDocumentFollowerService(webapp2.RequestHandler): 
    def get(self):
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        documentName = self.request.get('documentName')
        for document in documents:
            if document.documentName == documentName:
                break
        if(users.get_current_user().email() not in document.followers):
            document.followers.append(users.get_current_user().email())
            document.put()
        self.redirect('/ViewADocumentPage?documentName=' +document.documentName)
        
class AddDocumentFollowerFromAuthorService(webapp2.RequestHandler): 
    def get(self):
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        documentName = self.request.get('documentName')
        author = self.request.get('author')
        for document in documents:
            if document.author == author:
                if(users.get_current_user().email() not in document.followers):
                    document.followers.append(users.get_current_user().email())
                    document.put()
        self.redirect('/ViewADocumentPage?documentName=' +document.documentName)
        
class DeleteDocumentService(webapp2.RequestHandler): 
    def post(self):
        documentName = self.request.get('documentName')
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        for document in documents:
            if document.documentName == documentName:
                break
        document.key.delete()
        self.redirect('/ManagePage')
        
class UnFollowDocumentService(webapp2.RequestHandler): 
    def post(self):
        documentName = self.request.get('documentName')
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        for document in documents:
            if document.documentName == documentName:
                break
        document.followers.remove(users.get_current_user().email())
        document.put()
        self.redirect('/ManagePage')
        
class AddCommentOnCommentService(webapp2.RequestHandler): 
    def post(self):
        newComment = self.request.get('newComment')
        commentSymbol = self.request.get('commentSymbol')
        documentName = self.request.get('documentName')
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        for document in documents:
            if document.documentName == documentName:
                break
            
        if "C" in commentSymbol:
            if commentSymbol in document.commentOnCommentsList:
                document.commentOnCommentsList[commentSymbol].append(newComment)
            else:
                document.commentOnCommentsList[commentSymbol] = [newComment] 
        else:
            if commentSymbol in document.errorCommentOnCommentsList:
                document.errorCommentOnCommentsList[commentSymbol].append(newComment)
            else:
                document.errorCommentOnCommentsList[commentSymbol] = [newComment] 
            
#         document.commentOnCommentsList[commentSymbol] = [newComment]
        document.put()
        self.redirect('/ViewADocumentPage?documentName=%s' % documentName)
        
class UpVoteCommentService(webapp2.RequestHandler): 
    def post(self):
        commentSymbol = self.request.get('commentSymbol')
        documentName = self.request.get('documentName')
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        for document in documents:
            if document.documentName == documentName:
                break
        if "C" in commentSymbol:
            index = document.commentSymbol.index(commentSymbol)        
            document.commentVote[index] += 1
        else:
            index = document.errorSymbol.index(commentSymbol)        
            document.errorVote[index] += 1

        document.put()
        self.redirect('/ViewADocumentPage?documentName=%s' % documentName)
        
class DownVoteCommentService(webapp2.RequestHandler): 
    def post(self):
        commentSymbol = self.request.get('commentSymbol')
        documentName = self.request.get('documentName')
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        for document in documents:
            if document.documentName == documentName:
                break
        
        if "C" in commentSymbol:
            index = document.commentSymbol.index(commentSymbol)        
            document.commentVote[index] -= 1
        else:
            index = document.errorSymbol.index(commentSymbol)        
            document.errorVote[index] -= 1

        document.put()
        self.redirect('/ViewADocumentPage?documentName=%s' % documentName)
        
class AddCommentService(webapp2.RequestHandler): 
    def post(self):
        documentName = self.request.get('documentName')
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        for document in documents:
            if document.documentName == documentName:
                break
        titleString = self.request.get('titleString') 
        commentString= self.request.get('commentString') 
        relX= self.request.get('relX')
        relY= self.request.get('relY') 
        symbol= self.request.get('symbol') 
        if "C" in symbol: 
            document.commentList.insert(0,commentString)
            document.commentX.insert(0,relX)
            document.commentY.insert(0,relY)
            document.commentSymbol.insert(0,symbol)
            document.commentVote.insert(0,0)
            if(titleString == ""):
                document.commentTitle.insert(0,symbol)
            else:
                document.commentTitle.insert(0,titleString)
            document.commentCount +=1
        else:
            document.errorList.insert(0,commentString)
            document.errorX.insert(0,relX)
            document.errorY.insert(0,relY)
            document.errorSymbol.insert(0,symbol)
            document.errorVote.insert(0,0)
            if(titleString == ""):
                document.errorTitle.insert(0,symbol)
            else:
                document.errorTitle.insert(0,titleString)
            document.errorCount +=1
        document.put()
        self.redirect('/ViewADocumentPage?documentName=%s' % documentName)
        
class DeleteCommentService(webapp2.RequestHandler): 
    def post(self):
        documentName = self.request.get('documentName')
        documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
        documents = documents_query.fetch(1000)
        for document in documents:
            if document.documentName == documentName:
                break
        commentSymbol= self.request.get('commentSymbol') 
        if "C" in commentSymbol: 
            index = document.commentSymbol.index(commentSymbol)
            del document.commentList[index]
            del document.commentX[index]
            del document.commentY[index]
            del document.commentSymbol[index]
            del document.commentVote[index]
            del document.commentTitle[index]
        else:
            index = document.errorSymbol.index(commentSymbol)
            del document.errorList[index]
            del document.errorX[index]
            del document.errorY[index]
            del document.errorSymbol[index]
            del document.errorVote[index]
            del document.errorTitle[index]
        document.put()
        self.redirect('/ViewADocumentPage?documentName=%s' % documentName)


@ndb.transactional(retries=10)
def myUpload(documentName,imageKey):
    documents_query = Document.query(ancestor=document_key(ALL_DOCUMENTS_NAME)).order(-Document.date)
    documents = documents_query.fetch(1000)
    for document in documents:
        if document.documentName == documentName:
            break
    serving_url = images.get_serving_url(imageKey)
    serving_url = serving_url + "=s0"
    document.imageList.append(str(serving_url))
    document.put()

def cleanup(blob_keys):
    blobstore.delete(blob_keys)

class UploadHandler(webapp2.RequestHandler):

    def initialize(self, request, response):
        super(UploadHandler, self).initialize(request, response)
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Methods'
        ] = 'OPTIONS, HEAD, GET, POST, PUT, DELETE'
        self.response.headers[
            'Access-Control-Allow-Headers'
        ] = 'Content-Type, Content-Range, Content-Disposition'

    def validate(self, file):
        if file['size'] < MIN_FILE_SIZE:
            file['error'] = 'File is too small'
        elif file['size'] > MAX_FILE_SIZE:
            file['error'] = 'File is too big'
        elif not ACCEPT_FILE_TYPES.match(file['type']):
            file['error'] = 'Filetype not allowed'
        else:
            return True
        return False

    def get_file_size(self, file):
        file.seek(0, 2)  # Seek to the end of the file
        size = file.tell()  # Get the position of EOF
        file.seek(0)  # Reset the file position to the beginning
        return size

    def write_blobOLD(self, data, info):
        blob = files.blobstore.create(
            mime_type=info['type'],
            _blobinfo_uploaded_filename=info['name']
        )
        with files.open(blob, 'a') as f:
            f.write(data)
        files.finalize(blob)
        return files.blobstore.get_blob_key(blob)
    
#     @ndb.transactional


    def write_blob(self, data, info):
        documentName = self.request.get("documentName")
   
        blob = files.blobstore.create(
            mime_type=info['type'],
            _blobinfo_uploaded_filename=info['name']
        )
        with files.open(blob, 'a') as f:
            f.write(data)
        files.finalize(blob)     
        blobKey = files.blobstore.get_blob_key(blob)
        myUpload(documentName,blobKey)
        return files.blobstore.get_blob_key(blob)

    def handle_upload(self):
        results = []
        blob_keys = []
        for name, fieldStorage in self.request.POST.items():
            if type(fieldStorage) is unicode:
                continue
            result = {}
            result['name'] = re.sub(
                r'^.*\\',
                '',
                fieldStorage.filename
            )
            result['type'] = fieldStorage.type
            result['size'] = self.get_file_size(fieldStorage.file)
            if self.validate(result):
                print "------------------------------outside write_blob ------------------------------"
                time.sleep(.5)
                blob_key = str(
                    self.write_blob(fieldStorage.value, result)
                )
                
                    
                blob_keys.append(blob_key)
                result['deleteType'] = 'DELETE'
                result['deleteUrl'] = self.request.host_url +\
                    '/?key=' + urllib.quote(blob_key, '')
                if (IMAGE_TYPES.match(result['type'])):
                    try:
                        result['url'] = images.get_serving_url(
                            blob_key,
                            secure_url=self.request.host_url.startswith(
                                'https'
                            )
                        )
                        result['thumbnailUrl'] = result['url'] +\
                            THUMBNAIL_MODIFICATOR
                    except:  # Could not get an image serving url
                        pass
                if not 'url' in result:
                    result['url'] = self.request.host_url +\
                        '/' + blob_key + '/' + urllib.quote(
                            result['name'].encode('utf-8'), '')
            results.append(result)
#         deferred.defer(
#             cleanup,
#             blob_keys,
#             _countdown=EXPIRATION_TIME
#         )
        return results

    def options(self):
        pass

    def head(self):
        pass

    def get(self):
        pass
#         self.redirect('/search')
        
#         self.redirect(WEBSITE)

    def post(self):
        if (self.request.get('_method') == 'DELETE'):
            return self.delete()
        result = {'files': self.handle_upload()}
        s = json.dumps(result, separators=(',', ':'))
        redirect = self.request.get('redirect')
        if redirect:
            return self.redirect(str(
                redirect.replace('%s', urllib.quote(s, ''), 1)
            ))
        if 'application/json' in self.request.headers.get('Accept'):
            self.response.headers['Content-Type'] = 'application/json'
        self.response.write(s)

    def delete(self):
        key = self.request.get('key') or ''
        blobstore.delete(key)
        s = json.dumps({key: True}, separators=(',', ':'))
        if 'application/json' in self.request.headers.get('Accept'):
            self.response.headers['Content-Type'] = 'application/json'
        self.response.write(s)

application = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/ManagePage', ManagePage),
    ('/ViewADocumentPage', ViewADocumentPage),
    ('/ViewAllDocumentsPage', ViewAllDocumentsPage),
    ('/CreateDocumentPage', CreateDocumentPage),
    ('/SearchDocumentsPage', SearchDocumentsPage),
    ('/IncreaseDocumentCountService', IncreaseDocumentCountService),
    ('/DeleteDocumentService', DeleteDocumentService),
    ('/UnFollowDocumentService', UnFollowDocumentService),
    ('/CreateDocumentService', CreateDocumentService),
    ('/SearchDocumentService', SearchDocumentService),
    ('/AddDocumentFollowerService', AddDocumentFollowerService),
    ('/AddDocumentFollowerFromAuthorService', AddDocumentFollowerFromAuthorService),
    ('/AddCommentOnCommentService', AddCommentOnCommentService),
    ('/UpVoteCommentService', UpVoteCommentService),
    ('/DownVoteCommentService', DownVoteCommentService),
    ('/AddCommentService', AddCommentService),
    ('/DeleteCommentService', DeleteCommentService),
    ('/upload', UploadHandler),
    
], debug=True)


WEBSITE = 'https://blueimp.github.io/jQuery-File-Upload/'
MIN_FILE_SIZE = 1  # bytes
MAX_FILE_SIZE = 5000000  # bytes
IMAGE_TYPES = re.compile('image/(gif|p?jpeg|(x-)?png)')
ACCEPT_FILE_TYPES = IMAGE_TYPES
THUMBNAIL_MODIFICATOR = '=s80'  # max width / height
EXPIRATION_TIME = 300  # seconds




GOOD_UPLOADER_FIRST = """
    <!-- The file upload form used as target for the file upload widget -->
    <form id="fileupload" action="//jquery-file-upload.appspot.com/" method="POST" enctype="multipart/form-data">
        <!-- Redirect browsers with JavaScript disabled to the origin page -->
        <noscript><input type="hidden" name="redirect" value="https://blueimp.github.io/jQuery-File-Upload/"></noscript>
        <!-- The fileupload-buttonbar contains buttons to add/delete files and start/cancel the upload -->
        <div class="row fileupload-buttonbar">
            <div class="col-lg-7">
                <!-- The fileinput-button span is used to style the file input field as button -->
                <span style="width:23%%" class="btn btn-success fileinput-button" >
                   <!-- <i class="glyphicon glyphicon-plus"></i>
                    <span>Add files...</span>-->
                    <input  type="file" name="files[]" multiple>
                </span>
                <button type="submit" class="btn btn-primary start">
                    <i class="glyphicon glyphicon-upload"></i>
                    <span>Start upload</span>
                </button>
                <button type="reset" class="btn btn-warning cancel">
                    <i class="glyphicon glyphicon-ban-circle"></i>
                    <span>Cancel upload</span>
                </button>
                <button type="button" class="btn btn-danger delete">
                    <i class="glyphicon glyphicon-trash"></i>
                    <span>Delete</span>
                </button>
                <input type="checkbox" class="toggle">
                <!-- The global file processing state -->
                <span class="fileupload-process"></span>
            </div>
            <!-- The global progress state -->
            <div class="col-lg-5 fileupload-progress fade">
                <!-- The global progress bar -->
                <div class="progress progress-striped active" role="progressbar" aria-valuemin="0" aria-valuemax="100">
                    <div class="progress-bar progress-bar-success" style="width:0%;"></div>
                </div>
                <!-- The extended global progress state -->
                <div class="progress-extended">&nbsp;</div>
            </div>
        </div>
        <!-- The table listing the files available for upload/download -->
        <table role="presentation" class="table table-striped"><tbody class="files"></tbody></table>
    """
        

        
        
GOOD_UPLOADER_SECOND = """
    </form>
<!-- The blueimp Gallery widget -->
<div id="blueimp-gallery" class="blueimp-gallery blueimp-gallery-controls" data-filter=":even">
    <div class="slides"></div>
    <h3 class="title"></h3>
    <a class="prev"></a>
    <a class="next"></a>
    <a class="close"></a>
    <a class="play-pause"></a>
    <ol class="indicator"></ol>
</div>
<!-- The template to display files available for upload -->
<script id="template-upload" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-upload fade">
        <td>
            <span class="preview"></span>
        </td>
        <td>
            <p class="name">{%=file.name%}</p>
            <strong class="error text-danger"></strong>
        </td>
        <td>
            <p class="size">Processing...</p>
            <div class="progress progress-striped active" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="progress-bar progress-bar-success" style="width:0%;"></div></div>
        </td>
        <td>
            {% if (!i && !o.options.autoUpload) { %}
                <button class="btn btn-primary start" disabled>
                    <i class="glyphicon glyphicon-upload"></i>
                    <span>Start</span>
                </button>
            {% } %}
            {% if (!i) { %}
                <button class="btn btn-warning cancel">
                    <i class="glyphicon glyphicon-ban-circle"></i>
                    <span>Cancel</span>
                </button>
            {% } %}
        </td>
    </tr>
{% } %}
</script>
<!-- The template to display files available for download -->
<script id="template-download" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-download fade">
        <td>
            <span class="preview">
                {% if (file.thumbnailUrl) { %}
                    <a href="{%=file.url%}" title="{%=file.name%}" download="{%=file.name%}" data-gallery><img width="70" height="70" src="{%=file.thumbnailUrl%}"></a>
                {% } %}
            </span>
        </td>
        <td>
            <p class="name">
                {% if (file.url) { %}
                    <a href="{%=file.url%}" title="{%=file.name%}" download="{%=file.name%}" {%=file.thumbnailUrl?'data-gallery':''%}>{%=file.name%}</a>
                {% } else { %}
                    <span>{%=file.name%}</span>
                {% } %}
            </p>
            {% if (file.error) { %}
                <div><span class="label label-danger">Error</span> {%=file.error%}</div>
            {% } %}
        </td>
        <td>
            <span class="size">{%=o.formatFileSize(file.size)%}</span>
        </td>
        <td>
            {% if (file.deleteUrl) { %}
                <button class="btn btn-danger delete" data-type="{%=file.deleteType%}" data-url="{%=file.deleteUrl%}"{% if (file.deleteWithCredentials) { %} data-xhr-fields='{"withCredentials":true}'{% } %}>
                    <i class="glyphicon glyphicon-trash"></i>
                    <span>Delete</span>
                </button>
                <input type="checkbox" name="delete" value="1" class="toggle">
            {% } else { %}
                <button class="btn btn-warning cancel">
                    <i class="glyphicon glyphicon-ban-circle"></i>
                    <span>Cancel</span>
                </button>
            {% } %}
        </td>
    </tr>
{% } %}
</script>
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<!-- The jQuery UI widget factory, can be omitted if jQuery UI is already included -->
<script src="js/vendor/jquery.ui.widget.js"></script>
<!-- The Templates plugin is included to render the upload/download listings -->
<script src="//blueimp.github.io/JavaScript-Templates/js/tmpl.min.js"></script>
<!-- The Load Image plugin is included for the preview images and image resizing functionality -->
<script src="//blueimp.github.io/JavaScript-Load-Image/js/load-image.all.min.js"></script>
<!-- The Canvas to Blob plugin is included for image resizing functionality -->
<script src="//blueimp.github.io/JavaScript-Canvas-to-Blob/js/canvas-to-blob.min.js"></script>
<!-- Bootstrap JS is not required, but included for the responsive demo navigation 
<script src="//netdna.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>-->
<!-- blueimp Gallery script -->
<script src="//blueimp.github.io/Gallery/js/jquery.blueimp-gallery.min.js"></script>
<!-- The Iframe Transport is required for browsers without support for XHR file uploads -->
<script src="js/jquery.iframe-transport.js"></script>
<!-- The basic File Upload plugin -->
<script src="js/jquery.fileupload.js"></script>
<!-- The File Upload processing plugin -->
<script src="js/jquery.fileupload-process.js"></script>
<!-- The File Upload image preview & resize plugin -->
<script src="js/jquery.fileupload-image.js"></script>
<!-- The File Upload audio preview plugin -->
<script src="js/jquery.fileupload-audio.js"></script>
<!-- The File Upload video preview plugin -->
<script src="js/jquery.fileupload-video.js"></script>
<!-- The File Upload validation plugin -->
<script src="js/jquery.fileupload-validate.js"></script>
<!-- The File Upload user interface plugin -->
<script src="js/jquery.fileupload-ui.js"></script>
<!-- The main application script -->
<script src="js/main.js"></script>
<!-- The XDomainRequest Transport is included for cross-domain file deletion for IE 8 and IE 9 -->
<!--[if (gte IE 8)&(lt IE 10)]>
<script src="js/cors/jquery.xdr-transport.js"></script>
<![endif]-->
</body> 
</html>

"""