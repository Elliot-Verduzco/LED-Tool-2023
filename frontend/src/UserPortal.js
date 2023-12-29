// UserPortal.js
import React, { useState, useEffect } from 'react';

const UserPortal = () => {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        // Fetch orders from the backend
        const fetchOrders = async () => {
            const response = await fetch('/orders', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    // Include any authentication tokens if needed
                },
            });
            if (response.ok) {
                const data = await response.json();
                setOrders(data);
            }
        };

        fetchOrders();
    }, []);

    function fetchOrders() {

    }

    // Function to handle order creation
    const handleCreateOrder = async (orderData) => {
        const response = await fetch('/add_order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Include any authentication tokens if needed
            },
            body: JSON.stringify(orderData),
        });
        if (response.ok) {
            // Fetch the updated list of orders
            fetchOrders();
        }
    };

    return (
        <div>
            <h1>User Portal</h1>
            {/* Display list of orders */}
            <ul>
                {orders.map(order => (
                    <li key={order._id}>{order.name} - {order.status}</li>
                ))}
            </ul>
            {/* Add form or button to create a new order */}
            {/* This is a placeholder, implement the actual form based on your needs */}
            <button onClick={() => handleCreateOrder({ name: 'New Order', status: 'Pending' })}>
                Create Order
            </button>
        </div>
    );
}

export default UserPortal;
