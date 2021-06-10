statistics = [];
loaded = false;
modal = document.getElementById("myModal");

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
  container.style.height = "500px";
}

// When the user clicks on the button, open the modal
function openModal() {
  modal.style.display = "block";
  document.getElementById('network-content').innerHTML = "<div class='loader'></div>";
}

// When the user clicks on <span> (x), close the modal
function closeModal() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
} 
