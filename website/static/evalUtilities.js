const taskDescriptionsLong = [
  `Welcome to the Cauldron project! The tools on this website help to view, visualize and analye player and match data from the video game League Of Legends (LOL). LOL is a Multiplayer Online Battle Arena (MOBA) game where two teams, each consisting of 5 players, compete against each other in strategic matches.`,
  `View the provided tools in the different tabs and feel free to play around. Try to understand what they are for and how they can be used. When you are done, press the "Next Task" button on the bottom of the webpage.`,
  `Find out the age and IMI of the player with the id...`,
  `One player has got an exceptional high [Match/Network Feature]. Can you find out his [other feature]?`,
  `In elbow plots, the "elbow" in the curve determines the optimal k value for K-Means Clustering. What would k be if you want to cluster the player data by network features only?`,
  `View network graphs of the player with the ID 1149. Can you spot some features and derive information about that players play style or connections to the given numerical features?`,
  `Which player features do you think are most important for clustering? Which can be easily commited or may even distort a meaningful result? Which clustering method works best for you?`,
];

const taskDescriptionsShort = [
  `-`,
  `Task 1: Play around`,
  `Task 2: Get age and IMI of ...`,
  `Task 3: Get [other feature] of  the player with high [Match/Network Feature]`,
  `Task 4: Elbow Plots`,
  `Task 5: Network Features`,
  `Task 6: Clustering Parameters`,
];

function setTaskDescription(taskNumber) {
  document.getElementById("taskdesc").innerHTML = taskDescriptionsLong[taskNumber];
}

function setTaskDescriptionforClusteringPage(taskNumber) {
  document.getElementById("task-short").innerHTML = `${taskDescriptionsShort[taskNumber]} <div data-tip='${taskDescriptionsLong[taskNumber]}' class='qtip tip-top'><em class='fa fa-question-circle'></em></div>`;
}

