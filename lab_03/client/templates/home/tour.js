(function() {
  // Instance the tour
  var tour = new Tour({
    steps: [
      // {
      //   element: "#map-canvas",
      //   title: "Välkommen till trafikrapport.nu",
      //   content: "Kartan visar alla trafikrapporter som är rapporterade just nu."
      // },
      {
        element: "#info-box",
        title: "Informationsrutan",
        content: "Informationsrutan visar lite kort information om de olika markörerna på kartan."
      },
      {
        element: "#right-bar-icon",
        title: "Sidomenyn",
        content: "Sidomenyn innehåller så att man kan filtrera informationen via olika kategorier, se alla de rapporteringarna som finns på kartan fast i textform istället samt olika områden som olika trafikrapporter finns och även filtrera på dessa områden."
      }
    ]
  });

  // Initialize the tour
  tour.init();

  // Start the tour
  tour.start();
})();