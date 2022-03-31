export default class ContactService {
    static async insertContact(body) {
        try {
            const response = await fetch("/api/contacts", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            })
            return await response.json()
        } catch (error) {
            return console.log(error)
        }
    }

    static async updateContact(body, contact_id) {
        try {
            const response = await fetch(`/api/contacts/${contact_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            })
            return await response.json()
        } catch (error) {
            return console.log(error)
        }
    }

    static async deleteContact(contact_id) {
        try {
            const response = await fetch(`/api/contacts/${contact_id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: null
            })
            return await response.json()
        } catch (error) {
            return console.log(error)
        }
    }
}