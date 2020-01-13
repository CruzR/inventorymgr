(function() {
    function sendErrorReport(report) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/v1/errors/js', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify(report));
    }

    function handleError(message, source, lineno, colno, error) {
        var report = {
            location: document.location.toString(),
            message: message,
            source: source,
            lineno: lineno,
            colno: colno,
            stack: error.stack
        };
        sendErrorReport(report);
    }

    window.handleError = handleError;
    window.onerror = handleError;
})();
