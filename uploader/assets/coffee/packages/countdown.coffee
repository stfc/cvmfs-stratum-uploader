window.Packages = {}
window.Packages.initializeCountdown = (selector, initialDateTime) ->
  console.log($(selector).html())
  $(selector).countdown
    date: initialDateTime
    refresh: 1000
    render: (data) ->
      $(@el).text if data.days >= 1
        data.days + " day" + (if data.days > 1 then "s" else "")
      else if data.min >= 1
        @leadingZeros(data.hours,
          2) + " hour" + (if data.hours > 1 then "s" else "") + " " + @leadingZeros(data.min,
          2) + " min" + (if data.min > 1 then "s" else "")
      else
        @leadingZeros(data.sec, 2) + " second" + ((if data.sec > 1 then "s" else ""))
