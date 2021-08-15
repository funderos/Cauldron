let statistics = [];
let loaded = false;
let modal = document.getElementById("myModal");

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("collapsible-active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    } 
  });
}

function getStatArray() {
  return new Promise((resolve, reject) => {
    if (statistics.length) {
      resolve(statistics);
    } else {
      $.ajax({
        dataType: "json",
        url: "stats",
        success: function (data) {
          statistics = data;
          resolve(statistics);
        },
        error: function (error) {
          console.error("Error retrieving statistics.", error);
          reject();
        },
        timeout: 1000,
      });
    }
  });
}

function init() {
  document.getElementById("landingtab").style.display = "block";
  var chooser = document.getElementById('summonerid');
  chooser.options[chooser.selectedIndex].value;
}

function openTab(evt, tabId) {
  evt.currentTarget.className += " active";
  if (tabId == "statistics") {
    loadStatistics();
  }
  showTabContent(tabId);
}

function openTabManually(linkId, tabId) {
  document.getElementById(linkId).className += " active";
  showTabContent(tabId);
}

function showTabContent(tabId) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the link that opened the tab
  document.getElementById(tabId).style.display = "block";
}

// When the user clicks on the button, open the modal
function openModal() {
  modal.classList.add("modal-open");
}

// When the user clicks on <span> (x), close the modal
function closeModal() {
  modal.classList.remove("modal-open");
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
} 