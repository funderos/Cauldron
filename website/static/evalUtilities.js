const taskDescriptionsLong = [
  `This website provides the following analytic tools to analyze data from League Of Legends players:
  <ul>
    <li>Cluster players according to selected features with different algorithms</li>
    <li>Show ego network graphs of players in different sizes/modes</li>
    <li>Show statistics and cluster distributions of single features in boxplots</li>
    <li>Export cluster results and boxplot images</li>
  </ul>
  <br>
  When solving the following tasks, you will get to know the features provided while trying to find useful results of implicit and explicit nature.
  When you are done solving a task, fill out the task-specific fields and press the "Continue" button. These control inputs are limited to the tool evaluation and located in the red bar at the bottom of the page.`,
  `View the provided tools in the different tabs and feel free to play around. Try to understand what they are for and how they can be used.`,
  `Try to find out the Identified Regulation (IDE) value as well as the age of the player with ID 1273.`,
  `One player has got an exceptional high mean tie strength. Find out how many matches this player participated in are included in the used dataset.`,
  `Can you find common connections, dependencies or correlations between the psychological data and the social network data of the players? Use the clustering features of the tool for solving this task.`,
  `View the network graph of the player with the ID 1149. Can you spot some features and derive information about that player’s play style or social connections based on the given numerical features?`,
  `Which player features do you think are most important for clustering? Which can be easily omitted or may even distort a meaningful result? Which clustering method works best for you?`,
];

const taskDescriptionsShort = [
  `-`,
  `Task 1: Play around`,
  `Task 2: Get age and IDE of 1273`,
  `Task 3: Get match count from player with high mean tie strength`,
  `Task 4: Cluster data and find correlations`,
  `Task 5: View network graph of 1149 to derive playing habits`,
  `Task 6: Find useful clustering feature combinations`,
];

const surveyHeaders = [
  `<p>For the assessment of this tool, please fill out the following questionnaire. The questionnaire consists of pairs of contrasting attributes that may apply to the tool.
  The circles between the attributes represent gradations between the opposites. You can express your agreement with the attributes by ticking the circle that most closely reflects your impression. </p>
  <p>Please decide spontaneously. Don’t think too long about your decision to make sure that you convey your original impression.
  Sometimes you may not be completely sure about your agreement with  a particular attribute or you may find that the attribute does not apply completely to the particular product.
  Nevertheless, please tick a circle in every line. It is your personal opinion that counts. Please remember: there is no wrong or right answer! </p>
  <p>Please assess the product now by ticking one circle per line.</p>`,
  `For each of the following statements, please mark one box that best describes your reactions to the tool today.`,
  `Please answer the following questions with yes or no and optionally provide additional details in free text fields (depending on your answer).`,
  `Please provide some details about your person.`,
];

const ueq = [
  ["annoying", "enjoyable"],
  ["not understandable", "understandable"],
  ["creative", "dull"],
  ["easy to learn", "difficult to learn"],
  ["valuable", "inferior"],
  ["boring", "exciting"],
  ["not interesting", "interesting"],
  ["unpredictable", "predictable"],
  ["fast", "slow"],
  ["inventive", "conventional"],
  ["obstructive", "supportive"],
  ["good", "bad"],
  ["complicated", "easy"],
  ["unlikable", "pleasing"],
  ["usual", "leading edge"],
  ["unpleasant", "pleasant"],
  ["secure", "not secure"],
  ["motivating", "demotivating"],
  ["meets expectations", "does not meet expectations"],
  ["inefficient", "efficient"],
  ["clear", "confusing"],
  ["impractical", "practical"],
  ["organized", "cluttered"],
  ["attractive", "unattractive"],
  ["friendly", "unfriendly"],
  ["conservative", "innovative"],
];

const sus = [
  [
    "Strongly Disagree",
    "Strongly Agree",
    "I think that I would like to use the tool frequently.",
  ],
  [
    "Strongly Disagree",
    "Strongly Agree",
    "I found the tool unnecessarily complex.",
  ],
  [
    "Strongly Disagree",
    "Strongly Agree",
    "I thought the tool was easy to use.",
  ],
  [
    "Strongly Disagree",
    "Strongly Agree",
    "I think that I would need the support of a technical person to be able to use the tool.",
  ],
  [
    "Strongly Disagree",
    "Strongly Agree",
    "I found the various functions in the tool were well integrated.",
  ],
  [
    "Strongly Disagree",
    "Strongly Agree",
    "I thought there was too much inconsistency in the tool.",
  ],
  [
    "Strongly Disagree",
    "Strongly Agree",
    "I would imagine that most people would learn to use the tool very quickly.",
  ],
  [
    "Strongly Disagree",
    "Strongly Agree",
    "I found the tool very cumbersome (awkward) to use.",
  ],
  [
    "Strongly Disagree",
    "Strongly Agree",
    "I felt very confident using the tool.",
  ],
  [
    "Strongly Disagree",
    "Strongly Agree",
    "I needed to learn a lot of things before I could get going with the tool.",
  ],
];

const knowledgeScale = [
  ["No knowledge", "Expert", "Data Mining"],
  ["No knowledge", "Expert", "Data Analytics"],
  ["No knowledge", "Expert", "Social Network Analysis"],
  ["No knowledge", "Expert", "Player Communities in video games"],
  ["No knowledge", "Expert", "League Of Legends"]
]

const openQuestions = [
  [
    "Do you think that prior knowledge is required to use this tool?",
    "Which knowledge is required? (optional)",
  ],
  [
    "Did you have interesting findings when using this tool?",
    "Which findings did you have? (optional)",
  ],
  [
    "Are there specific domains and/or use cases of this tool that can you think of?",
    "Please sepcify (optional)",
  ],
  [
    "Did you miss any functionality or features when using this tool?",
    "Pleasy specify (optional)",
  ],
  ["Would you like to give us some additional feedback?", "Pleasy sepcify"],
];

function setTaskDescription(progress) {
  document.getElementById(
    "taskdesc"
  ).innerHTML = `<p>${taskDescriptionsLong[progress]}</p>`;
}

function setSurveyContent(progress) {
  document.getElementById("survey-header").innerHTML = `<p>${
    surveyHeaders[progress - 7]
  }</p>`;

  let surveyDiv = document.getElementById("survey-div");
  switch (progress) {
    case 7:
      surveyDiv.innerHTML = getSurveyTable(progress, 7, ueq, false);
      break;
    case 8:
      surveyDiv.innerHTML = getSurveyTable(progress, 5, sus, true);
      break;
    case 9:
      surveyDiv.innerHTML = getOpenQuestions();
      break;
    case 10:
      surveyDiv.innerHTML = getPersonDetails();
      break;
    default:
      console.error("Unkknown progress value for survey page: " + progress);
  }
}

function getPersonDetails() {
  const radioString = "&nbsp;&nbsp; <label><input type='radio' name='10.7' onChange='setFieldVisibility(10, ";
  return "<p><b>Age: </b><input type='number' min='0' name='10.6' class='txtfd txtfd-small' required /></p>"
  + "<p><b>Gender:</b>" + radioString + "false)' value='w' required />&nbsp;Woman</label>"
  + radioString + "false)' value='m' required />&nbsp;Man</label>"
  + radioString + "false)' value='n' required />&nbsp;Non-binary</label>"
  + radioString + "false)' value='u' required />&nbsp;Prefer not to disclose</label>"
  + radioString + "true)' value='c' required />&nbsp;Prefer to self-describe</label></p>"
  + "<p><textarea id='txt10' name='10.7t' placeholder='Please specify' class='txtarea open-hidden'></textarea></p>"
  + "<p><b>For each of the following domains, please mark one box that best describes your prior knowledge in this domain:</b></p>"
  + getSurveyTable(10, 5, knowledgeScale, true);
}

function getOpenQuestions() {
  let htmlString = "";
  let i = 1;
  for (let question of openQuestions) {
    htmlString =
      htmlString +
      "<p><b>" +
      question[0] +
      "</b> &nbsp;&nbsp; <label><input type='radio' name='9." +
      i +
      "' value='y' " +
      "onChange='setFieldVisibility(9" +
      i +
      ", true)' required /> Yes</label> &nbsp; <label><input type='radio' " +
      "name='9." +
      i +
      "' value='n' onChange='setFieldVisibility(9" +
      i +
      ", false)' required /> No</label></p><p><textarea id='txt9" +
      i +
      "' name='9." +
      i +
      "t' placeholder='" +
      question[1] +
      "' class='txtarea open-hidden'></textarea></p>";
    i++;
  }
  return htmlString;
}

function setFieldVisibility(questionNumber, visible) {
  document.getElementById("txt" + questionNumber).className = visible
    ? "txtarea open-visible"
    : "txtarea open-hidden";
}

function getSurveyTable(progress, count, fields, additionalSpace = false) {
  return (
    "<table>" +
    getHeaderFieldString(count, additionalSpace) +
    getBodyFieldsString(fields, count, progress) +
    "</table>"
  );
}

function getHeaderFieldString(count, additionalSpace = false) {
  let headers;
  if (additionalSpace) {
    headers =
      "<tr><th class='wide'></th><th class='text-right width-130'></th>";
  } else {
    headers = "<tr><th class='text-right'></th>";
  }
  for (let i = 1; i <= count; i++) {
    headers = headers + "<th class='radio'>" + i + "</th>";
  }
  if (additionalSpace) {
    headers = headers + "<th class='text-left width-110'></th></tr>";
  } else {
    headers = headers + "<th></th></tr>";
  }
  return headers;
}

function getBodyFieldsString(fields, count, progress) {
  let scale = "";
  let j = 1;
  for (const prompt of fields) {
    if (prompt.length > 2) {
      scale =
        scale +
        "<tr><td>" +
        prompt[2] +
        "</td><td class='text-right'>" +
        prompt[0] +
        "</td>";
    } else {
      scale = scale + "<tr><td class='text-right'>" + prompt[0] + "</td>";
    }
    let nameString = " name='" + progress + "." + j + "' required /></td>";
    for (let i = 1; i <= count; i++) {
      scale =
        scale + "<td class='radio'><input type='radio' value=" + i + nameString;
    }
    scale = scale + "<td class='text-left'>" + prompt[1] + "</td></tr>";
    j++;
  }
  return scale;
}

function setTaskDescriptionforClusteringPage(taskNumber) {
  document.getElementById(
    "task-short"
  ).innerHTML = `${taskDescriptionsShort[taskNumber]} <div data-tip='${taskDescriptionsLong[taskNumber]}' class='qtip tip-top'><em class='fa fa-question-circle'></em></div>`;

  if (taskNumber == 6) {
    (function ($) {
      var CheckboxDropdown = function (el) {
        var _this = this;
        this.isOpen = false;
        this.$el = $(el);
        this.$label = this.$el.find(".dropdown-label");
        this.$inputs = this.$el.find('[type="checkbox"]');

        //this.onCheckBox(singleSelect);

        this.$label.on("click", function (e) {
          e.preventDefault();
          _this.toggleOpen();
        });

        this.$inputs.on("change", function (e) {
          var $box = $(this);
          if ($box.attr("singleSelect")) {
            if ($box.is(":checked")) {
              _this.$inputs.prop("checked", false);
              _this.$inputs.removeAttr("required");
              $box.prop("checked", true);
            } else {
              _this.$inputs.attr("required", "required");
              $box.prop("checked", false);
            }
            _this.onCheckBox(true);
          } else {
            _this.onCheckBox(false);
          }
        });
      };

      CheckboxDropdown.prototype.onCheckBox = function (singleSelect) {
        this.updateStatus(singleSelect);
      };

      CheckboxDropdown.prototype.updateStatus = function (
        singleSelect = false
      ) {
        var checked = this.$el.find(":checked");

        if (checked.length === this.$inputs.length) {
          this.$label.html(this.$label.attr("value") + " (All Selected)");
        } else {
          var stringEnd = singleSelect ? "/1 Selected)" : " Selected)";
          this.$label.html(
            this.$label.attr("value") + " (" + checked.length + stringEnd
          );
        }
      };

      CheckboxDropdown.prototype.toggleOpen = function (forceOpen) {
        var _this = this;

        if (!this.isOpen || forceOpen) {
          this.isOpen = true;
          this.$el.addClass("on");
          $(document).on("click", function (e) {
            if (!$(e.target).closest("[data-control]").length) {
              _this.toggleOpen();
            }
          });
        } else {
          this.isOpen = false;
          this.$el.removeClass("on");
          $(document).off("click");
        }
      };

      var checkboxesDropdowns = document.querySelectorAll(
        '[data-control="checkbox-dropdown"]'
      );
      for (var i = 0, length = checkboxesDropdowns.length; i < length; i++) {
        new CheckboxDropdown(checkboxesDropdowns[i]);
      }
    })(jQuery);
  }
}
