import boto
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import HTMLQuestion
import os.path 
import sys 
from random import shuffle 
from variables import aws_access_key, aws_secret_key, host, form, result

# Create connection to MTurk
mtc = MTurkConnection(aws_access_key_id=aws_access_key,
aws_secret_access_key=aws_secret_key,
host=host)

lines_control = []  
lines_data = []
infile_control = 'Control_Text.txt'
infile_data = sys.argv[1]

topics = ['American Holidays', 'Earth Facts', 'Land Animals', 'Health', 'Technology'] 
filename = os.path.splitext(infile_data)[0] 
date = filename.split("_")[4] + "_" + filename.split("_")[5] + "_" + filename.split("_")[6] 

description_to_topic = {
	'Boston Marathon Bombing': 'In April 2013, two homemade bombs detonated 12 seconds and 210 yards (190 m) apart at 2:49 p.m., near the finish line of the annual Boston Marathon', 
	'Midwest Tornados': 'The tornado outbreak of May 18–21, 2013 was a significant tornado outbreak that affected parts of the Midwestern United States and lower Great Plains.', 
	'NSA File Leak':'In June 2013, Edward Snowden, a former Central Intelligence Agency employee, and former contractor for the United States government, copied and leaked classified information from the National Security Agency (NSA) in 2013 without authorization.',
	'Ghouta (Syria) Chemical Weapon Attack': 'Chemical attack that occurred in Ghouta, Syria during the Syrian Civil War, in August 2013. Two opposition-controlled areas in the suburbs around Damascus, Syria were struck by rockets containing the chemical agent sarin.', 
	'Khan Shaykhun (Syria) Chemical Weapon Attack':'In April 2017, a chemical weapons attack occured in Khan Shyakhun, Syria.', 
	'Ransomware Cyber Attack': 'In May 2017, a worldwide Cyberattack in which a cryptoworm targeted computers running the Microsoft Windows by encrypting data and demanding ransom payments in the Bitcoin cryptocurrency occured.',
	'Hurricane Maria':'In September 2017, a Category 5 Hurricane hit many islands in the Caribbean.', 
	'Las Vegas Mass Shooting':'In October 2017, a gunman opened fire on a crowd of concertgoers at the Route 91 Harvest music festival on the Las Vegas Strip in Nevada. ' 
}

dates_to_topic = {
	'2013_04_15':'Boston Marathon Bombing',
	'2013_04_16':'Boston Marathon Bombing',
	'04_16_copy':'Boston Marathon Bombing', 
	'2013_04_17':'Boston Marathon Bombing', 
	'2013_04_18':'Boston Marathon Bombing', 
	'2013_04_19':'Boston Marathon Bombing', 
	'2013_04_20':'Boston Marathon Bombing',
	'2013_04_21':'Boston Marathon Bombing', 
	'2013_05_19':'Midwest Tornados', 
	'2013_05_20':'Midwest Tornados',
	'2013_05_21':'Midwest Tornados',
	'2013_05_22':'Midwest Tornados',
	'2013_05_23':'Midwest Tornados',  
	'2013_05_24':'Midwest Tornados',
	'2013_05_25':'Midwest Tornados',
	'2013_06_09':'NSA File Leak', 
	'2013_06_10':'NSA File Leak',
	'2013_06_11':'NSA File Leak',
	'2013_06_12':'NSA File Leak',
	'2013_06_13':'NSA File Leak',  
	'2013_06_14':'NSA File Leak',
	'2013_08_22':'Ghouta (Syria) Chemical Weapon Attack', 
	'2013_08_23':'Ghouta (Syria) Chemical Weapon Attack',
	'2013_08_24':'Ghouta (Syria) Chemical Weapon Attack',
	'2013_08_25':'Ghouta (Syria) Chemical Weapon Attack',
	'2013_08_26':'Ghouta (Syria) Chemical Weapon Attack',  
	'2013_08_27':'Ghouta (Syria) Chemical Weapon Attack',
	'2013_08_28':'Ghouta (Syria) Chemical Weapon Attack',
	'2017_04_04':'Khan Shaykhun (Syria) Chemical Weapon Attack',
	'2017_04_05':'Khan Shaykhun (Syria) Chemical Weapon Attack',
	'2017_04_06':'Khan Shaykhun (Syria) Chemical Weapon Attack',
	'2017_04_07':'Khan Shaykhun (Syria) Chemical Weapon Attack',
	'2017_04_08':'Khan Shaykhun (Syria) Chemical Weapon Attack',
	'2017_04_09':'Khan Shaykhun (Syria) Chemical Weapon Attack',
	'2017_04_10':'Khan Shaykhun (Syria) Chemical Weapon Attack',
	'2017_05_12':'Ransomware Cyber Attack',
	'2017_05_13':'Ransomware Cyber Attack',
	'2017_05_14':'Ransomware Cyber Attack',
	'2017_05_15':'Ransomware Cyber Attack',
	'2017_05_16':'Ransomware Cyber Attack',
	'2017_05_17':'Ransomware Cyber Attack',
	'2017_09_20':'Hurricane Maria',
	'2017_09_21':'Hurricane Maria',
	'2017_09_22':'Hurricane Maria',
	'2017_09_23':'Hurricane Maria',
	'2017_09_24':'Hurricane Maria',
	'2017_09_25':'Hurricane Maria',
	'2017_09_26':'Hurricane Maria',
	'2017_10_02':'Las Vegas Mass Shooting',
	'2017_10_03':'Las Vegas Mass Shooting',
	'2017_10_04':'Las Vegas Mass Shooting',
	'2017_10_05':'Las Vegas Mass Shooting',
	'2017_10_06':'Las Vegas Mass Shooting',
	'2017_10_07':'Las Vegas Mass Shooting'
}

with open(infile_control) as f:
	control = f.read().splitlines()
	lines_control.extend(control)
with open(infile_data) as f_in:
	data = f_in.read().split('\n\n') 
	for d in data:
		m = d.replace('\n',' ') 
		lines_data.append(m)  

shuffle(lines_data)

survey_html = '<h2>Categorize a few sample sentences to get warmed up!</h2>'
count = 0	

#generate html for control questions
for l in lines_control:
	print(l)
	if(l != ''):
		if count < len(topics): 
			topic = topics[count]
		field = str(count) + "-c"
		field_id_zero = str(count) + "-0"
		field_id_one = str(count) + "-1" 
		survey_html += """
		        <h4>Topic: """+topic+"""</h4>
				<p class="text">"""+l+"""</p>
				<div>
		         <fieldset>
		            <label style="position:inline-block;margin-bottom:5px;">
		                  <div class="radiowrapper green" style="position:inline-block;">
		                  <input type="radio" name='"""+field+"""' class="btTxt """+field_id_zero+"""" id='"""+field_id_zero+"""' value="Directly discusses topic" required>
		                  <label for='"""+field_id_zero+"""'>Fact</label>
		              </div>
		            </label>
		            <label style="position:inline-block;">
		                  <div class="radiowrapper yellow" style="position:inline-block;">
		                  <input type="radio" name='"""+field+"""' class="btTxt """+field_id_one+"""" id= """+field_id_one+""" value="Not relevant to topic">
		                  <label for='"""+field_id_one+"""'>Context</label>
		              </div>
		            </label>
		          </fieldset>
		          </div>"""
			
		count += 1


 
#generate html for the sentences in the transcripts that are being tested    
topic = dates_to_topic[date]
survey_html += """
<h2>Now it's time to categorize the sentences!</h2>
<h3> The topic is: """+topic +"""</h3>
<p>"""+ description_to_topic[topic] +""" </p>  
<div style="position:relative;">
"""

num_sentences = 0
for l in lines_data:
	print(l)
	if(l != ''):
		field = str(count) + "-q"
		field_id_zero = str(count) + "-0"
		field_id_one = str(count) + "-1" 
		if num_sentences == 0:
			div_string = """<div style="position:absolute;top:0px;" class=""" +str(num_sentences) +""">"""
		else:
			div_string = """<div style="position:absolute;top:0px;" class="hideMe """ + str(num_sentences)  + """">""" 
		survey_html += div_string
		survey_html += """
		  <p class="text">"""+l+""" ("""+ str(num_sentences) + """/""" + str(len(lines_data)) + """) </p>
			<div>
	         <fieldset>
	            <label>
	                  <div class="radiowrapper green" style="position:inline-block;margin-bottom:5px;">
	                  <input type="radio" name='"""+field+"""' class="btTxt """+field_id_zero+"""" id='"""+field_id_zero+"""' value="Directly discusses topic" onclick="show_next('"""+str(num_sentences) +"""')" required>
	                  <label for='"""+field_id_zero+"""'>Fact</label>
	              </div>
	            </label>
	            <label>
	                  <div class="radiowrapper yellow" style="position:inline-block;">
	                  <input type="radio" name='"""+field+"""' class="btTxt """+field_id_one+"""" id= """+field_id_one+""" onclick="show_next('"""+str(num_sentences) +"""')" value="Not relevant to topic">
	                  <label for='"""+field_id_one+"""'>Context</label>
	              </div>
	            </label>
	          </fieldset>
	          </div>
	      </div>
          <br />"""
		if(num_sentences == (len(lines_data)-1)):
			survey_html += """<p><strong>Make sure that you have filled out ALL of the demographic questions. HIT will not submit otherwise</strong><p>
<p><input type='submit' id='submitButton' value='Submit' /></p> """
		num_sentences += 1
		count += 1

survey_html += "</div>"

#This variable actually creates the form that will be put on MTurk and contains the bulk of information.
#Variable contains the html, css and questions that don't change from person to person
#Test your design in an html file before testing in the sandbox environment. 
question_html_value = """
<html>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>
<script src='https://s3.amazonaws.com/mturk-public/externalHIT_v1.js' type='text/javascript'></script> 
<script src='https://s3.amazonaws.com/slantometer-files/bootstrap.min.css' type='style/css'></script>
<script src='https://s3.amazonaws.com/slantometer-files/jquery-3.2.1.min.js' type='text/javascript'></script>
<script src="//uniqueturker.myleott.com/lib.js" type="text/javascript"></script>
<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>

<link href="https://fonts.googleapis.com/css?family=Lato:300i,700i" rel="stylesheet">
<link href="https://fonts.googleapis.com/css?family=Coming+Soon" rel="stylesheet">
<style type="text/css">
    body {
      margin: 0;
      font-family: 'Lato', sans-serif;
    }

    .btn-group{
      vertical-align: center;
      margin-bottom: 40px;
    }

    #text-option{
      font-family: 'Coming Soon', cursive;
    }

    #body{
      display: "none";
    }

    #box1,#box2, #box3, #box4{
      display: "none"; 
      width: 700px;
      height: 600px; 
      left: 20%;
      top: 20%;
      margin-bottom: 50px;
      position: absolute;
      font-family: 'Lato', sans-serif;
      border: 1px solid black;
      overflow: scroll;
      text-align: center;
    }

    select{
      font-family: 'Lato', sans-serif;
    }

    option{
      font-family: 'Lato', sans-serif;
    }

    #box1 > h1{
      text-align: center;
    }

    #box1 > h4{
      text-align: center;
    }

    #box2{
      display: "none"; 
      width: 600px;
      height: 600px; 
      left: 20%;
      top: 20%;
      position: absolute; 
      border: 1px solid black;
    }

    #box3{
      display: "none"; 
      width: 600px;
      height: 600px; 
      left: 20%;
      top: 20%;
      position: absolute; 
      border: 1px solid black;
    }

    .text{
      font-family: 'Lato:700i', sans-serif;
    }

    input{
      text-align: center;
      white-space: normal;
    }

    .correct{
      color:green;
      display: "none";
    }

    .incorrect{
      color: red;
    }
    #overflow{
      position: absolute;
      overflow: hidden; 
    }

    #section{
      margin-top: 50px;
      margin-bottom: 50px;
    }

    img{
      width: 50px;
      height: 50px;
    }

    
    label > input{ /* HIDE RADIO */
	    visibility: hidden; /* Makes input not-clickable */
	    position: absolute; /* Remove input from document flow */
	    font-family: 'Lato', sans-serif;
	  }

	 .hideMe{
	    display:none;
	  }

	  .showMe{
	    display:block;
	  }

	  label > input + img{ /* IMAGE STYLES */
	    cursor:pointer;
	    border:2px solid transparent;
	    width: 50px;
	    height: 50px;
	     text-align: center;
	     font-family: 'Lato', sans-serif;

	  }
	  label > input:checked + img{ /* (RADIO CHECKED) IMAGE STYLES */
	    border:2px solid #000;
	     text-align: center;
	     font-family: 'Lato', sans-serif;

	  }

    .radiowrapper {position:inline-block;font-family: 'Lato', sans-serif;}
    .radiowrapper input {visibility:hidden; width:0;}
	.radiowrapper label:hover {font-weight:bold}
	.green label{border: 2px solid #90EE90;position:inline-block;}
	.yellow label{border: 2px solid #FFFF66;position:inline-block;}
	.green label:hover {font-weight:bold; border: 2px solid #90EE90;}
	.yellow label:hover {font-weight:bold; border: 2px solid #FFFF66;}
	.plain label:hover {font-weight:bold; border: 2px solid black;}
	.radiowrapper.green label:checked + label {font-weight:bold; border: 2px solid #90EE90;}
	.radiowrapper.yellow label:checked + label  {font-weight:bold; border: 2px solid #FFFF66;}
	.radiowrapper input:checked + label {border: 2px solid #000;}

    .selected{
      background-color: #DCDCDC;
    }

    .chosen{
      border: 2px solid #4682B4;
    }

    .checkboxgroup {
	  display: inline-block;
	  text-align: center;
	}
	.checkboxgroup label {
	  display: block;
	}

	.checkboxgroup input {
	  visibility: hidden;
	  cursor:pointer;
	  border:2px solid transparent;
	}

	.menu figure {display: inline-block; margin:10px; padding:0px; font-family: 'Lato', sans-serif;}

	label > input + img{ /* IMAGE STYLES */
	    
	    width: 50px;
	    height: 50px;
	     text-align: center;

	  }
	  
	  .checkboxgroup label > input:checked + img{ /* (RADIO CHECKED) IMAGE STYLES */
	    border:2px solid #000;
	     text-align: center;

	  }

    .image-btn:hover
    {
      -moz-box-shadow: 0px 0px 10px #ccc;
      -webkit-box-shadow: 0px 0px 10px #ccc;
      box-shadow: 0px 0px 10px #ccc;
    }

    .image-btn-tv:hover
    {
      -moz-box-shadow: 0px 0px 10px #ccc;
      -webkit-box-shadow: 0px 0px 10px #ccc;
      box-shadow: 0px 0px 10px #ccc;
    }
  </style>
  <script type="text/javascript">
    function fillInLanguages() { 
      var states= ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut","District of Columbia",
                      "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana",
                      "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana",
                      "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio",
                      "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee",
                      "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin","West Virginia","Wyoming"];
      var state_abbrev = [ "AK","AL", "AR", "AS", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "GU", "HI", "IA", "ID", "IL", "IN",
                          "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM",
                          "NV", "NY", "OH", "OK", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT",
                          "VA", "VI", "VT","WA","WI","WV","WY"];
      for (var i = 0; i < states.length; i++) {
        document.writeln("<option value='" + state_abbrev[i] + "'>" + states[i] + "</option>");
      }
    }

    function fillInEducation() {
      var states= ["High School Diploma or Equivalent", "Associate's Degree", "Bachelor's Degree", "Master's Degree", "Doctoral Degree"];
      for (var i = 0; i < states.length; i++) {
        document.writeln("<option value='" + states[i] + "'>" + states[i] + "</option>");
      }
    }

	$('input[type="button"]').click(function(){
	    $(this).addClass('chosen');
	});

	$('input[type="image"]').click(function(){
	    $(this).addClass('chosen');
	});

    function show_next(count){ 
	    num = Number(count);
	    $("." + num).addClass("hideMe");
	    $("." + (num+1)).removeClass("hideMe");
	}

	$(document).ready(function() {
	    $('form').submit(function() {
	        var incomplete = $('form :input').filter(function() {
	                             return $(this).val() == '';
	                         });
	        //if incomplete contains any elements, the form has not been filled 
	        if(incomplete.length) {
	            alert('Please make sure all fields filled out');
	            //to prevent submission of the form
	            return false;
	        }
	     });
	});
	(function(){
	    var ut_id = "f8ed5768a0f586e635412745568ddf7e";
	    if (UTWorkerLimitReached(ut_id)) {
	        document.getElementById('mturk_form').style.display = 'none';
	        document.getElementsByTagName('body')[0].innerHTML = "You have already completed the maximum number of HITs allowed by this requester. Please click 'Return HIT' to avoid any impact on your approval rating.";
	    }
	})();
	function disabler_text(number){
	  $("#" + number).attr('disabled', true);
	  $("#" + number).toggleClass( "selected" );
	}
  </script>
</head>
<body>
<!-- HTML to handle creating the HIT form -->
<form name='mturk_form' method='post' id='mturk_form' action="""+form+""">
<input type='hidden' value='' name='assignmentId' id='assignmentId'/>
<!-- This is where you define your question(s) --> 
<div class="wrapper">

<div class="cell">

<div align="center"><h1>Sentence Classification Test</h1></div> 


<h2>Instructions</h2>
<p>In this study, you will be shown 20 sentences from a broadcast news transcript. For each sentence, please determine how the sentence helps create your understanding of the topic. </p>
<p>If the sentence provides information on who, what, when and where about the given topic, then categorize the sentence as 'Fact'. Such sentences often include numbers, dates, times, names, locations, quotes from videos and people, descriptions of actions, and details about an event.</p>
<p>If the sentence gives information on why or how the topic occurred, then categorize the sentence as 'Context'. Such sentences often include lots of adjectives, opionated language and information about related topics and events.</p>
<p><strong>Remember that you must ACCEPT the hit before you can submit the results. Submit button will appear after you have completed all the questions. Please do not do this HIT more than once.</strong></p> 

</div>


<div class="cell">
      <div id="section1">
        <h2>But first ... tell us about yourself!</h2> 
        <h4> How old are you? </h4>
         
        <fieldset> 
        <div class="container">
	        <label class="radio-inline">
		        <div class="radiowrapper" style="position:inline-block;">
		            <input type="radio" name="saveForm" class="btTxt submit image-btn" id="<20" value="<20" required/>
		            <label for="<20"> Younger than 20 </label>
		        </div>
	        </label>
			<label class="radio-inline">
		        <div class="radiowrapper" style="position:inline-block;">
		            <input type="radio" name="saveForm" class="btTxt submit image-btn" id="20-30" value="20-30" />
		            <label for="20-30"> 21-30 </label>
		        </div>
	        </label>
			<label class="radio-inline">
		        <div class="radiowrapper" style="position:inline-block;">
		            <input type="radio" name="saveForm" class="btTxt submit image-btn" id="31-40" value="31-40" />
		            <label for="31-40"> 31-40 </label>
		        </div>
	        </label>
			<label class="radio-inline">
		        <div class="radiowrapper" style="position:inline-block;">
		            <input type="radio" name="saveForm" class="btTxt submit image-btn" id="41-50" value="41-50" />
		            <label for="41-50"> 41-50 </label>
		        </div>
	        </label>
			<label class="radio-inline">
		        <div class="radiowrapper" style="position:inline-block;">
		            <input type="radio" name="saveForm" class="btTxt submit image-btn" id="51-60" value="51-60" />
		            <label for="51-60"> 51-60 </label>
		        </div>
	        </label>
			<label class="radio-inline">
		        <div class="radiowrapper" style="position:inline-block;">
		            <input type="radio" name="saveForm" class="btTxt submit image-btn" id="61-70" value="61-70" />
		            <label for="61-70"> 61-70 </label>
		        </div>
	        </label>
			<label class="radio-inline">
		        <div class="radiowrapper">
		            <input type="radio" name="saveForm" class="btTxt submit image-btn" id="71+" value="71+" />
		            <label for="71+"> 71+ </label>
		        </div>
	        </label> 
	        </div>
		</fieldset>

        <h4> Are you male or female? </h4>
		<fieldset>
			<section class="menu">
	        <figure>
	          <label>
	            <input type="radio" name="gender" value="female" id="female" required/>
	            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Pink_Venus_symbol.svg/400px-Pink_Venus_symbol.svg.png">
	            <figcaption>Female</figcaption>
	           </label>
	        </figure>
	        <figure>
	          <label>
	            <input type="radio" name="gender" value="male" id="male" />
	            <img src="http://pngimages.net/sites/default/files/blue-male-symbols-png-image-100562.png">
	            <figcaption>Male</figcaption>
	           </label>
	        </figure>
	     	<figure>
              <label>
		        <div class="radiowrapper" style="position:inline-block;">
		            <input type="radio" name="gender" value="Other" id="Other">
		            <label for="Other">Other</label>
		        </div>
		      </label>
	        </figure>
			</section>
		</fieldset>
	     
         

        <h4> Where are you from? </h4>
        <select name="language1" id="lang1" required> 
            <option selected="selected" value="default" >Please select</option>
            <script>fillInLanguages()</script>
        </select>


        <h4> What is the highest level of education that you have completed or are currently pursuing? </h4>
        <select name="eduaction" id="ed" required> 
            <option selected="selected" value="default" >Please select</option>
            <script>fillInEducation()</script>
        </select>
      </div>

      <div id="section2">
        <h2> Let's talk politics </h2> 

        <h4> Do you align with a particular political party? </h4>
          <fieldset>
			<section class="menu">
	        <figure>
	          <label>
	            <input type="radio" name="party" value="republican" id="republican" required/>
	            <img src="https://sites.google.com/site/politicalpartiesanalysis/political-parties/political-party-symbols/Republicanlogo.svg.png">
	            <figcaption>Republican</figcaption>
	           </label>
	        </figure>
	        <figure>
	          <label>
	            <input type="radio" name="party" value="Democratic" id="Democratic" />
	            <img src="http://d3n8a8pro7vhmx.cloudfront.net/dplac/sites/1/meta_images/original/dem-donkey-right-copy.png?1413244000">
	            <figcaption>Democratic</figcaption>
	           </label>
	        </figure>
	     	<figure>
	          <label>
	            <input type="radio" name="party" value="green" id="green" />
	            <img src="https://upload.wikimedia.org/wikipedia/commons/9/9a/Libertarian_Party_Porcupine_%28USA%29.svg">
	            <figcaption>Green</figcaption>
	           </label>
	        </figure>
	        <figure>
	          <label>
	            <input type="radio" name="party" value="Libertarian" id="Libertarian" />
	            <img src="https://upload.wikimedia.org/wikipedia/en/thumb/1/11/Green_Party_of_the_United_States_Earthflower_Official_Logo.png/187px-Green_Party_of_the_United_States_Earthflower_Official_Logo.png">
	            <figcaption>Libertarian</figcaption>
	           </label>
	        </figure>
	        <figure>
	          <label>
	            <input type="radio" name="party" value="Constitution" id="Constitution" />
	            <img src="http://votecp.com/wp-content/uploads/2017/04/LogoOnly.gif">
	            <figcaption>Constitution</figcaption>
	           </label>
	        </figure>
	        <figure>
              <label>
		        <div class="radiowrapper" style="position:inline-block;">
		            <input type="radio" name="party" value="Independent" id="Independent">
		            <label for="Independent">Independent</label>
		        </div>
		      </label>
	        </figure>
			</section>
		</fieldset>
      

	      <h4> Are you registered to vote? </h4>
	      	<fieldset>
			<section class="menu">
	        <figure style="margin-right:15px;">
	          <label>
	            <input type="radio" name="vote" value="yes" id="yes" required />
	            <img src="https://thumbs.dreamstime.com/b/happy-uncle-sam-19429232.jpg">
	            <figcaption>Yes</figcaption>
	           </label>
	        </figure>
	        <figure style="margin-right:15px;">
	          <label>
	            <input type="radio" name="vote" value="no" id="no" />
	            <img src="https://thumbs.dreamstime.com/b/sad-uncle-sam-19429228.jpg">
	            <figcaption>No</figcaption>
	           </label>
	        </figure>
			</section>
			</fieldset>
      </div>

      <div id="section3">
        <h1> Television habits </h1> 

       <h4> How many days a week do you watch televised broadcast news?</h4>
       <fieldset> 
        <div class="container">
	        <label class="radio-inline">
		        <div class="radiowrapper" style="position:inline-block;">
		            <input type="radio" name="tv" class="btTxt submit image-btn" id="0" value="0" required />
		            <label for="0"> 0 </label>
		        </div>
	        </label>
			<label class="radio-inline">
		        <div class="radiowrapper" style="position:inline-block;">
		            <input type="radio" name="tv" class="btTxt submit image-btn" id="1" value="1" />
		            <label for="1"> 1</label>
		        </div>
	        </label>
			<label class="radio-inline">
		        <div class="radiowrapper" style="position:inline-block;">
		            <input type="radio" name="tv" class="btTxt submit image-btn" id="2" value="2" />
		            <label for="2"> 2</label>
		        </div>
	        </label>
			<label class="radio-inline">
		        <div class="radiowrapper" style="position:inline-block;">
		            <input type="radio" name="tv" class="btTxt submit image-btn" id="3" value="3" />
		            <label for="3"> 3 </label>
		        </div>
	        </label>
			<label class="radio-inline">
		        <div class="radiowrapper" style="position:inline-block;">
		            <input type="radio" name="tv" class="btTxt submit image-btn" id="4" value="4" />
		            <label for="4"> 4 </label>
		        </div>
	        </label>
			<label class="radio-inline">
		        <div class="radiowrapper" style="position:inline-block;">
		            <input type="radio" name="tv" class="btTxt submit image-btn" id="5" value="5" />
		            <label for="5"> 5</label>
		        </div>
	        </label>
			<label class="radio-inline">
		        <div class="radiowrapper">
		            <input type="radio" name="saveForm" class="btTxt submit image-btn" id="6" value="6" />
		            <label for="6"> 6 </label>
		        </div>
	        </label> 
	        <label class="radio-inline">
		        <div class="radiowrapper">
		            <input type="radio" name="saveForm" class="btTxt submit image-btn" id="7" value="7" />
		            <label for="7"> 7 </label>
		        </div>
	        </label>
	        </div>
		</fieldset>
	  </div>
  </div>

"""+ survey_html + """


</div>


<!-- HTML to handle submitting the HIT -->
</form>
<script language='Javascript'>turkSetAssignmentID();</script>
</body>
</html>
"""

# The first parameter is the HTML content
# The second is the height of the frame it will be shown in
# Check out the documentation on HTMLQuestion for more details
html_question = HTMLQuestion(question_html_value, 1000)

# These parameters define the HIT that will be created
# question is what we defined above
# max_assignments is the # of unique Workers you're requesting
# title, description, and keywords help Workers find your HIT
# duration is the # of seconds Workers have to complete your HIT
# reward is what Workers will be paid when you approve their work
# Check out the documentation on CreateHIT for more details

try:
	response = mtc.create_hit(question=html_question,
	                          max_assignments=9,
	                          title="Rank sentences from broadcast news",
	                          description="Help research a topic",
	                          keywords="question, answer, research",
	                          duration=3600,
	                          reward=0.15)
except BaseException as e:
	print(e)


# response includes data that can be used to retrieve information once workers have completed the HIT
hit_type_id = response[0].HITTypeId
hit_id = response[0].HITId #extract HITId
csv_line = infile_data + "," + hit_id + "\n" 
out_f = open('mturk_hit_Ids_need_payment.txt','a') #write HITId and associated file name to output file
out_f.write(csv_line)
out_f.close()

print("Your HIT has been created. You can see it at this link:")
print(result.format(hit_type_id))
print("Your HIT ID is: {}".format(hit_id))
