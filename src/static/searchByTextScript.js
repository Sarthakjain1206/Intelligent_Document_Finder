let allDictionaryData;
let dictionaryTitles;
let dictionaryText;
let dictionarySummary;
let dictionaryTags;
let dictionaryExtensions;

let currentTitle;
let currentText;
let currentSummary;
let currentTags;
let currentExtension;
let icon_location;

let the_one_tag;

$(document).ready(function(){
  //console.log("ready");



  //console.log($('.just_the_outer').height());
  let completeHeight = $('body').height();
  //console.group(completeHeight);
  $('.show_similar_overlay').css({"height": completeHeight});

  $('.submitButton').on('click', function(){
    let mainText = $(this).parent().parent().parent().find("div:eq(0)").next();
    let mainHeading = mainText.find("div:eq(0)");
    let mainForm = mainHeading.find("form:eq(0)");
    let mainTitle = mainForm.find("button:eq(0)").val();
    //console.log(mainTitle);
    let mainInput = $(this).parent().find("input:eq(0)").val(mainTitle);
    let mainInputVal = mainInput.val();
    //console.log(mainInputVal);

    req = $.ajax({
      url : '/acceptTitle',
      type : 'POST',
      data : {mainInputVal : mainInputVal}
    });

    

    req.done(function(data){
      //console.log("done");
      //console.log(data.returnData);
      allDictionaryData = data.returnData;

      dictionaryTitles = allDictionaryData.titles;
      dictionaryText = allDictionaryData.text;
      dictionarySummary = allDictionaryData.summary;
      dictionaryTags = allDictionaryData.tags;
      dictionaryExtensions = allDictionaryData.extension;


      for(var i = 0 ; i < 9; i++){
          //console.log("Title: " + allDictionaryData.titles[i]);
          //console.log("Text: " + allDictionaryData.text[i]);
          //console.log("Summary: " + allDictionaryData.summary[i]);
          //console.log("Tags: " + allDictionaryData.tags[i]);
  
          currentTitle = allDictionaryData.titles[i];
          currentText = allDictionaryData.text[i];
          currentSummary = allDictionaryData.summary[i];
          currentTags = allDictionaryData.tags[i];
          currentExtension = allDictionaryData.extension[i];
          icon_location = "static/icons/"+currentExtension + ".svg";
          

          the_one_tag = currentTags[Math.floor(Math.random() * currentTags.length)];

          the_second_tag = currentTags[Math.floor(Math.random() * currentTags.length)]; 
 
          document.getElementById("show_similar_outer_container").innerHTML += `<div class="output_holder" id="show_similar_output_holder" style = "margin-top:5vh">
          <div class="output">
              <div class="file_extension_ico">
                  <div class="img_holder">
                  <img src="${icon_location}">
                  </div>
              </div>
  
              <div class="text">
                  <div class="heading" id="heading">
  
                      <form action="/filenameonclick" , method="POST">
                          <input type="text" onchange="seeif()"  name="file_head" class="thehiddenforminput"  id="thehiddenform">
                          <button type="submit" id="myclassnameid" name="myclassname" class="myclassname" value="${currentTitle}"><b>Title: </b><span>${currentTitle}</span></button>
                      </form>
                  </div>
  
                  <div class="original_text">
                    <b style="font-size: 2.2vh">Text: </b>  ${currentText}
                  </div>
                  <div class="tags">
  
                      <div class="tag_container">
                          <div style="padding: 1vh 1vh;"><b>Tags: </b></div>
                          <div class="final_tags">
                                  <div class="the_tag" id="the_tag_holder" style="display:flex; flex-direction: row">
                                    
                                    <li>${the_one_tag}</li>
                                    <li>${the_second_tag}</li>
                                  </div>
                          </div>
                      </div>
                  </div>
              </div>
  
              <div class="summary" style="padding-bottom: 2vh;padding-right: 3vw">
                  <p style="text-align:center; font-weight: 500; font-size: 2.3vh">Summary</p>
                  ${currentSummary}
                  
              </div>
  
          </div>
  
          
         
  
  
      </div>`;


      }
      
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
  document.getElementById('show_similar_outer_container').innerHTML = "";
}







