class FinanceAPI {
    constructor() {
        this.baseURL = '/api';
        this.token = localStorage.getItem('access_token');
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        if (this.token) {
            config.headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }
    
    // Auth methods
    async login(email, password) {
        const data = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        if (data.access_token) {
            this.token = data.access_token;
            localStorage.setItem('access_token', this.token);
        }
        
        return data;
    }
    
    async register(username, email, password) {
        const data = await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password })
        });
        
        if (data.access_token) {
            this.token = data.access_token;
            localStorage.setItem('access_token', this.token);
        }
        
        return data;
    }
    
    logout() {
        this.token = null;
        localStorage.removeItem('access_token');
    }
    
    // Transaction methods
    async getTransactions() {
        return this.request('/transactions');
    }
    
    async createTransaction(transactionData) {
        return this.request('/transactions', {
            method: 'POST',
            body: JSON.stringify(transactionData)
        });
    }
}

// Create global API instance
window.financeAPI = new FinanceAPI();
