
/*
 * Editor client script for DB table schedules
 * Created by http://editor.datatables.net/generator
 */

(function($){

$(document).ready(function() {
	var editor = new $.fn.dataTable.Editor( {
		ajax: '/api/schedules',
		table: '#schedules',
		fields: [
			{
				"label": "Lesson:",
				"name": "lesson"
			},
			{
				"label": "Teacher:",
				"name": "teacher"
			},
			{
				"label": "Language:",
				"name": "language"
			},
			{
				"label": "Date:",
				"name": "date",
				"type": "datetime",
				"format": "DD\/MM\/YY HH:mm"
			}
		]
	} );

	var table = $('#schedules').DataTable( {
		dom: 'Bfrtip',
		ajax: '/api/schedules',
		columns: [
			{
				"data": "lesson"
			},
			{
				"data": "teacher"
			},
			{
				"data": "language"
			},
			{
				"data": "date"
			}
		],
		select: true,
		lengthChange: false,
		buttons: [
			{ extend: 'create', editor: editor },
			{ extend: 'edit',   editor: editor },
			{ extend: 'remove', editor: editor }
		]
	} );
} );

}(jQuery));

