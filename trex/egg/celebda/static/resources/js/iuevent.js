var IUEvent = {
    initScrollEventData: function () {

        for (var selector in scrollData) {
            if (scrollData.hasOwnProperty(selector) == false) {
                continue;
            }
            // get elements
            var eventData = scrollData[selector];
            var el = document.querySelector(selector);

            // set attribute
            for (var eName in eventData) {
                if (eventData.hasOwnProperty(eName) == false) {
                    continue;
                }
                var eValue = eventData[eName];
                el.setAttribute(eName, eValue);
            }
        }
    }
}
