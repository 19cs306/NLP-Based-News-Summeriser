function myFunction() {
	var x = document.getElementById("myTopnav");
	if (x.className === "topnav") {
	  x.className += " responsive";
	} else {
	  x.className = "topnav";
	}
  }
  var checkList = document.getElementById("list1");
  checkList.getElementsByClassName("anchor")[0].onclick = function (evt) {
	if (checkList.classList.contains("visible"))
	  checkList.classList.remove("visible");
	else checkList.classList.add("visible");
  };
  // Get the checkbox input elements
  var checkboxes = document.querySelectorAll(
	"#filter-options input[type='checkbox']"
  );
  
  // Get all the anchor tags in the content
  var anchors = document.querySelectorAll("#content a");
  
  // Add event listener to the checkboxes
  for (var i = 0; i < checkboxes.length; i++) {
	checkboxes[i].addEventListener("change", function () {
	  // Get the checked options
	  var checkedOptions = [];
	  for (var j = 0; j < checkboxes.length; j++) {
		if (checkboxes[j].checked) {
		  checkedOptions.push(checkboxes[j].value.toLowerCase());
		}
	  }
  
	  // Loop through all the anchor tags
	  for (var k = 0; k < anchors.length; k++) {
		// Get the href attribute value and convert to lowercase
		var href = anchors[k].getAttribute("href").toLowerCase();
  
		// Check if the href contains any of the checked options
		var matchFound = false;
		for (var l = 0; l < checkedOptions.length; l++) {
		  if (href.indexOf(checkedOptions[l]) !== -1) {
			matchFound = true;
			break;
		  }
		}
  
		// Show or hide the anchor tag based on the checked options
		if (checkedOptions.length === 0 || matchFound) {
		  anchors[k].parentNode.style.display = "";
		} else {
		  anchors[k].parentNode.style.display = "none";
		}
	  }
	});
  }
  var list1 = document.getElementById("list1");
  window.addEventListener('scroll', function() {
	if (window.scrollY > 0) {
	  list1.classList.remove('visible');
	}
  });