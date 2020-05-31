

function show_filter_menu(){
    document.getElementById('the_outer_wrapper').style.display = "block";
    document.getElementById('complete_body_overlay').style.display ="block";
    //disableScroll();
}


function close_filter_menu(){
    document.getElementById('the_outer_wrapper').style.display = "none";
    document.getElementById('complete_body_overlay').style.display ="none";

    document.getElementById('selected_button').classList.remove("filter_button");
    document.getElementById('selected_button').innerHTML = "";
    document.getElementById('selected_button').style.display = "none";

    //enableScroll();
}

var filter_type ;

function apply_filter(){
    
    var the_correct_placeholder;
    the_correct_placeholder = filter_type;
    type1 = "Search by Relevance";
    type2 = "Search by Tag";
    type3 = "Search by Title";

    if(the_correct_placeholder == type1){
      document.getElementById('search_bar').placeholder = "Enter text to search...";
    }
    else if(the_correct_placeholder == type2){
      document.getElementById('search_bar').placeholder = "Enter tag to search...";
    }
    else{
      document.getElementById('search_bar').placeholder = "Enter title to search...";
    }
    document.getElementById('filter_type_name_holder').value = the_correct_placeholder;
    close_filter_menu();
}

function select_this_type(obj){
    filter_type =  obj.innerHTML;
    //console.log(filter_type);
    document.getElementById('selected_button').classList.add("filter_button");
    document.getElementById('selected_button').innerHTML = filter_type;
    document.getElementById('selected_button').style.display = "block";
}

function empty_search(){
    document.getElementById('search_bar').value = "";
}



var keys = {37: 1, 38: 1, 39: 1, 40: 1};

function preventDefault(e) {
  e.preventDefault();
}

function preventDefaultForScrollKeys(e) {
  if (keys[e.keyCode]) {
    preventDefault(e);
    return false;
  }
}

// modern Chrome requires { passive: false } when adding event
var supportsPassive = false;
try {
  window.addEventListener("test", null, Object.defineProperty({}, 'passive', {
    get: function () { supportsPassive = true; } 
  }));
} catch(e) {}

var wheelOpt = supportsPassive ? { passive: false } : false;
var wheelEvent = 'onwheel' in document.createElement('div') ? 'wheel' : 'mousewheel';

// call this to Disable
function disableScroll() {
  window.addEventListener('DOMMouseScroll', preventDefault, false); // older FF
  window.addEventListener(wheelEvent, preventDefault, wheelOpt); // modern desktop
  window.addEventListener('touchmove', preventDefault, wheelOpt); // mobile
  window.addEventListener('keydown', preventDefaultForScrollKeys, false);
}

// call this to Enable
function enableScroll() {
  window.removeEventListener('DOMMouseScroll', preventDefault, false);
  window.removeEventListener(wheelEvent, preventDefault, wheelOpt); 
  window.removeEventListener('touchmove', preventDefault, wheelOpt);
  window.removeEventListener('keydown', preventDefaultForScrollKeys, false);
}




$(document).ready(function(){

  
    
  var scrollLink = $('.scroll');

  scrollLink.click(function(e){
      e.preventDefault();
      //console.log("success");
      $('body,html').animate({
          scrollTop: $(this.hash).offset().top
      }, 1000)
  });

  let completeHeight = $('body').height();
  //console.group(completeHeight);
  $('.complete_body_overlay').css({"height": completeHeight});


  let the_exception_value
  the_exception_value = $('.exception_text_holder').val();
  if(the_exception_value == 1){
    //alert("Document uploaded successfully!");
    $('.file_status').text("File uploaded successfully!");
    document.getElementById('file_status_outer').style.display = "block";
    $('.exception_text_holder').val("0");
  }
  else if(the_exception_value == -1){
    //alert("Unable to upload document!");
    $('.file_status').text("Unable to upload file :(");
    document.getElementById('file_status_outer').style.display = "block";
    $('.exception_text_holder').val("0");
   
  }
  else{
    //nothing
  }

});

function thefunc(){ 
  let entered_vale_of_tag = document.getElementById("files_tags_upload_entry").value;
  //console.log(entered_vale_of_tag);
  document.getElementById('the_tag_id').value = entered_vale_of_tag
}


function close_file_status(){
  document.getElementById('file_upload_status').style.display = "none";
}

