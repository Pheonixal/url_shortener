function copyToClipboard() {
    var copyText = document.getElementById("short-url");
    var fullLink = window.location.origin + '/' + copyText.value;
    navigator.clipboard.writeText(fullLink)
        .then(function() {
            alert("URL copied to clipboard!");
        })
        .catch(function(error) {
            console.error("Failed to copy URL to clipboard: ", error);
        });
}