class APIService {
    
    async GetResults(body) {
        const response = await fetch('http://localhost:8000/results', {
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