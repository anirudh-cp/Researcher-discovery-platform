class APIService {
    
    async GetResults(body) {
        const apiUrl = process.env.REACT_APP_API_URL;

        console.log(apiUrl);
        console.log(process.env)
        const response = await fetch(apiUrl + '/results', {
            'method': 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        })
        return await response.json()
    }
}

export default APIService