$(document).ready ->
  $(".timepicker").timepicker
    showSeconds: true
    showMeridian: false
    defaultTime: false
    minuteStep: 1
    secondStep: 1

  $(".datepicker").datetimepicker
    pickTime: false

  $(".select2").select2()

  $("#line_subscriber_report_form form").submit (e) ->
    $("#line_subscriber_report_form").modal("hide")
    return

  $("#line_service_report_form form").submit (e) ->
    $("#line_service_report_form").modal("hide")
    return

  $("#ccaa_report_form form").submit (e) ->
    $("#ccaa_report_form").modal("hide")
    return
