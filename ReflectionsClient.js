/** I'm not using this properly and consistently, even :-P */
var reflectiondiv = $(".reflection");

/** List of student names */
var students = [];

/** List of assignments the server knows about */
var assignments = [];

/** Index to the list of student names */
var i = 0;

/** 
 * Round to closest 10
 */
var roundInt = function(i) {
	return Math.round(i / 10) * 10;
}

/**
 * Load assignments asynchronously, and load the first one
 */
jQuery.getJSON("/listassignments", function(data) {
	assignments = data;
	assignments.forEach(function(a) {
		var o = new Option(a, a);
		o.innerHTML = a;
		$("#assignmentselector").append(o);
	});
	$("#assignmentselector").change(function() {
		jQuery.getJSON("/liststudents?a=" + $("#assignmentselector").val(), function(data) {
			students = data;
		nextStudent(0);
		});
	});
	/** Initialize before the user has provided any interactions */
	$("#assignmentselector").val(assignments[0]);
	$("#assignmentselector").trigger("change");
});

/**
 * Progress along the list of students. For UI buttons
 * 
 * @param {Integer} s - Steps to progress, typically 1 or -1.
 */
var nextStudent = function(s) {
	/** constrain the index values */
	i = i + s;
	i < 0 ? i = 0 : false;
	i >= students.length ? i = students.length - 1 : false;
	$("#studentname").text(students[i]);
	loadStudent(i, $(".reflection"));
}

/**
 * Loads the student by index in the students variable
 * 
 * @param {number} i - Student index.
 * @param {(HTMLElement|string)} e - HTML element to replace, or CSS selector.
 */
var loadStudent = function(i, e) {
	console.log("Loading " + students[i]);
	$.get("/student?s=" + students[i] + "&a=" + $("#assignmentselector").val(), function(data) {
		$(e).replaceWith(data);
		$("#refllength").text("≈ " + roundInt($(".reflection").text().split(" ").length) + " words");
	});
}
