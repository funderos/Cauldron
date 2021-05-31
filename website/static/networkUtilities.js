statistics = [];
loaded = false;

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

function openTab(evt, tabId) {
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
  evt.currentTarget.className += " active";
  setHeight();
}

function setHeight() {
  var container = document.getElementById("network-content");
  container.style.height = container.offsetWidth * 0.75 + "px";
}
