const SPREADSHEET_ID = '1_MEtfMgdIVsE82R_BSGE9cbGQtw4JWRz1uSTZzEuqQM'; // Replace with your actual Google Sheet ID
const RANGE = 'MAIN SHEET'; // Replace with your sheet name or range

// Load the Google Sheets API
function initClient() {
    gapi.client.init({
        apiKey: 'mnst-isc-key.json', // Replace with your API key
        discoveryDocs: ['https://sheets.googleapis.com/$discovery/rest?version=v4'],
    }).then(() => {
        // Fetch data from the Google Sheet
        fetchData();
    });
}

// Fetch data from the Google Sheet
function fetchData() {
    gapi.client.sheets.spreadsheets.values.get({
        spreadsheetId: SPREADSHEET_ID,
        range: RANGE,
    }).then(response => {
        const values = response.result.values;
        const headers = values[0];
        const data = values.slice(1).map(row => {
            return headers.reduce((obj, header, index) => {
                obj[header] = row[index];
                return obj;
            }, {});
        });

        console.log(sizes); 
        // Update sneakers with the fetched data
        sneakers.length = 0;
        Array.prototype.push.apply(sneakers, data);

        // Populate Size dropdown
        const sizes = [...new Set(sneakers.map(sneaker => sneaker.Size))];
        const sizeDropdown = $("#size");
        sizeDropdown.empty();
        sizeDropdown.append('<option value="">All Sizes</option>');
        sizes.forEach(size => sizeDropdown.append(`<option value="${size}">${size}</option>`));

        // Display the initial catalog
        displayCatalog(sneakers);
    });
}

// Initialize the API client and fetch data when the page loads
gapi.load('client', initClient);
