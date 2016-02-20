var count = 0;
$(document).ready(function () {
	$("#CommentButton").click(function(){
//		alert('Click On the Document to Make a Message');
		$("#firstImage").click(function(e){
//			alert('clicked me');
		   var parentOffset = $(this).parent().offset(); 
		   //or $(this).offset(); if you really just want the current element's offset
		   var relX = e.pageX - parentOffset.left;
		   var relY = e.pageY - parentOffset.top;
		   var form = '<form action="/AddCommentService" method="post"> <input  type="text" class="fixedLocationComment" name="commentString"/>\
			   <input type="hidden" name="relX" value="' +relX+ '"/> <input type="hidden" name="relY" value="' +relY+ '"/> \
			   <input type="hidden" name="symbol" value="c' +count+ '"/>\
           <div><input type="submit" class="btn btn-default fixedLocationCommentConfirm" value="Confirm Comment"></div>  \
           </form>'
			var txt1 = '<input  type="text" class="fixedLocationComment"/>';               // Create element with HTML
			var p = '<form action="/" method="get"><input type="submit" id="p' +count+'"'+ 'class="fixedLocationP" value="c'+count+'"/></form>';
//			 +'relx ='+relX  + 'rely =' +relY+ '</div>'
			
		    $("body").append(form,p);         // Append the new elements 
		    
//		    $("#hello").attr("position","fixed");
//		    $("#hello").attr("left",relX);
//		    $("#hello").attr("top",relY);
		    $("#p" + count).css({ 'position': 'absolute','left':relX, 'top':relY , 'opacity':0.5});
//		    $("#hello").style.position = "absolute";
//		    $("#hello").style.left = relX;
//		    $("#hello").style.top = relX;
		    count +=1;
		    $("#firstImage").off();
		});
	});
});
