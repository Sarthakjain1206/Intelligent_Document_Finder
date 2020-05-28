$(document).ready(function(){
  console.log("ready");

  //console.log($('.just_the_outer').height());
  let completeHeight = $('body').height();
  console.group(completeHeight);
  $('.show_similar_overlay').css({"height": completeHeight});

  $('.submitButton').on('click', function(){
    let mainText = $(this).parent().parent().parent().find("div:eq(0)").next();
    let mainHeading = mainText.find("div:eq(0)");
    let mainForm = mainHeading.find("form:eq(0)");
    let mainTitle = mainForm.find("button:eq(0)").val();
    //console.log(mainTitle);
    let mainInput = $(this).parent().find("input:eq(0)").val(mainTitle);
    let mainInputVal = mainInput.val();
    console.log(mainInputVal);

    req = $.ajax({
      url : '/acceptTitle',
      type : 'POST',
      data : {mainInputVal : mainInputVal}
    });

    req.done(function(data){
      console.log("done");
    });

    $('.show_similar_span').text(mainInputVal);
    $('.show_similar_overlay').css({"display" : "block"});

  });

});


function open_overlay(){
  document.getElementById('show_similar_overlay').style.display = "block";
}



function close_overlay(){
  document.getElementById('show_similar_overlay').style.display = "none";
}















