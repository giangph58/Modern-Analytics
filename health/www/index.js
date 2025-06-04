$(() => {
  Shiny.addCustomMessageHandler("toggleActiveTab", (payload) => {
    // Hide all tabs first
    $(".page-main").removeClass("main-visible");
    
    // Show only the requested tab
    $("#" + payload.activeTab + "-container").addClass("main-visible");
  });
});