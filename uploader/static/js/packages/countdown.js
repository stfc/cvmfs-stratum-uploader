(function() {
  window.Packages = {};

  window.Packages.initializeCountdown = function(selector, initialDateTime) {
    console.log($(selector).html());
    return $(selector).countdown({
      date: initialDateTime,
      refresh: 1000,
      render: function(data) {
        return $(this.el).text(data.days >= 1 ? data.days + " day" + (data.days > 1 ? "s" : "") : data.min >= 1 ? this.leadingZeros(data.hours, 2) + " hour" + (data.hours > 1 ? "s" : "") + " " + this.leadingZeros(data.min, 2) + " min" + (data.min > 1 ? "s" : "") : this.leadingZeros(data.sec, 2) + " second" + (data.sec > 1 ? "s" : ""));
      }
    });
  };

}).call(this);
