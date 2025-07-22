<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mail - DAZZLE PREMIUM</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #1d1d1f;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            overflow-x: hidden;
        }

        .app-container {
            display: flex;
            min-height: 100vh;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            gap: 20px;
            align-items: stretch;
        }

        .sidebar {
            flex: 1;
            max-width: 320px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            display: flex;
            flex-direction: column;
            height: fit-content;
            min-height: calc(100vh - 40px);
        }

        .main-panel {
            flex: 2;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            display: flex;
            flex-direction: column;
            min-height: calc(100vh - 40px);
        }

        .app-header {
            text-align: center;
            margin-bottom: 40px;
        }

        .app-title {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #007AFF, #5856D6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }

        .app-subtitle {
            color: #86868b;
            font-size: 1.1rem;
            font-weight: 500;
        }

        .section-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: #1d1d1f;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .section-icon {
            width: 24px;
            height: 24px;
            background: linear-gradient(135deg, #007AFF, #5856D6);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.9rem;
        }

        .date-display {
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
            padding: 25px;
            border-radius: 16px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .current-date {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1d1d1f;
            margin-bottom: 5px;
        }

        .current-time {
            font-size: 1rem;
            color: #86868b;
            font-weight: 500;
        }

        .missing-info {
            background: linear-gradient(135deg, #FFE4B5, #FFEAA7);
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 30px;
            border-left: 4px solid #FF6B35;
        }

        .missing-info h3 {
            color: #D63031;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .missing-list {
            list-style: none;
        }

        .missing-list li {
            color: #2D3436;
            font-size: 0.95rem;
            margin-bottom: 5px;
            padding-left: 20px;
            position: relative;
        }

        .missing-list li:before {
            content: "•";
            color: #FF6B35;
            font-weight: bold;
            position: absolute;
            left: 0;
        }

        .mail-compose {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .compose-header {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 25px;
            border-radius: 16px;
            margin-bottom: 25px;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-label {
            display: block;
            font-size: 0.95rem;
            font-weight: 600;
            color: #1d1d1f;
            margin-bottom: 8px;
        }

        .form-input {
            width: 100%;
            padding: 15px 18px;
            border: 2px solid #e5e5e7;
            border-radius: 12px;
            font-size: 1rem;
            font-family: inherit;
            background: white;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }

        .form-input:focus {
            outline: none;
            border-color: #007AFF;
            box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
            transform: translateY(-1px);
        }

        .form-input::placeholder {
            color: #86868b;
        }

        .compose-body {
            flex: 1;
            margin-bottom: 25px;
        }

        .body-textarea {
            width: 100%;
            min-height: 400px;
            padding: 20px;
            border: 2px solid #e5e5e7;
            border-radius: 16px;
            font-size: 1rem;
            font-family: inherit;
            background: white;
            resize: vertical;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
            line-height: 1.6;
        }

        .body-textarea:focus {
            outline: none;
            border-color: #007AFF;
            box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
        }

        .action-buttons {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }

        .btn {
            flex: 1;
            padding: 16px 24px;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            font-family: inherit;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }

        .btn:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }

        .btn:hover:before {
            left: 100%;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
        }

        .btn:active {
            transform: translateY(0);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .btn-primary {
            background: linear-gradient(135deg, #007AFF, #5856D6);
            color: white;
        }

        .btn-secondary {
            background: linear-gradient(135deg, #FF6B35, #FF8E53);
            color: white;
        }

        .btn-tertiary {
            background: linear-gradient(135deg, #00D2FF, #3A7BD5);
            color: white;
        }

        .paste-area {
            background: #f5f5f7;
            border: 2px dashed #d1d1d6;
            border-radius: 16px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            transition: all 0.3s ease;
        }

        .paste-area:hover {
            background: #ebebed;
            border-color: #007AFF;
        }

        .paste-instruction {
            color: #86868b;
            font-size: 1.1rem;
            font-weight: 500;
            margin-bottom: 15px;
        }

        .paste-textarea {
            width: 100%;
            min-height: 200px;
            padding: 20px;
            border: none;
            border-radius: 12px;
            background: white;
            font-size: 0.95rem;
            font-family: 'SF Mono', Monaco, monospace;
            resize: vertical;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .paste-textarea:focus {
            outline: none;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05), 0 0 0 3px rgba(0, 122, 255, 0.1);
        }

        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: rgba(52, 199, 89, 0.1);
            color: #34C759;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 20px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: #34C759;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }

        .glass-effect {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .floating-elements {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }

        .floating-circle {
            position: absolute;
            border-radius: 50%;
            background: linear-gradient(135deg, rgba(0, 122, 255, 0.1), rgba(88, 86, 214, 0.1));
            animation: float 20s infinite ease-in-out;
        }

        .floating-circle:nth-child(1) {
            width: 300px;
            height: 300px;
            top: 10%;
            left: 10%;
            animation-delay: 0s;
        }

        .floating-circle:nth-child(2) {
            width: 200px;
            height: 200px;
            top: 60%;
            right: 10%;
            animation-delay: -10s;
        }

        .floating-circle:nth-child(3) {
            width: 150px;
            height: 150px;
            bottom: 20%;
            left: 30%;
            animation-delay: -5s;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            25% { transform: translateY(-20px) rotate(5deg); }
            50% { transform: translateY(10px) rotate(-5deg); }
            75% { transform: translateY(-10px) rotate(3deg); }
        }

        @media (max-width: 1024px) {
            .app-container {
                flex-direction: column;
                padding: 15px;
                gap: 15px;
            }
            
            .sidebar {
                max-width: none;
                min-height: auto;
                order: 2;
            }
            
            .main-panel {
                order: 1;
                min-height: auto;
            }
            
            .action-buttons {
                flex-direction: column;
            }
        }

        .tooltip {
            position: relative;
            display: inline-block;
        }

        .tooltip::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.85rem;
            white-space: nowrap;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
            margin-bottom: 8px;
        }

        .tooltip:hover::after {
            opacity: 1;
        }
    </style>
</head>
<body>
    <div class="floating-elements">
        <div class="floating-circle"></div>
        <div class="floating-circle"></div>
        <div class="floating-circle"></div>
    </div>

    <div class="app-container">
        <!-- Left Sidebar -->
        <div class="sidebar">
            <div class="app-header">
                <h1 class="app-title">Mail</h1>
                <p class="app-subtitle">DAZZLE PREMIUM</p>
            </div>

            <div class="date-display">
                <div class="current-date" id="currentDate"></div>
                <div class="current-time" id="currentTime"></div>
            </div>

            <div class="section-title">
                <div class="section-icon">📧</div>
                Mail Information
            </div>

            <div id="missingInfoSection" class="missing-info" style="display: none;">
                <h3>⚠️ Missing Information</h3>
                <ul id="missingInfoList" class="missing-list"></ul>
            </div>

            <div class="paste-area">
                <div class="paste-instruction">📋 Paste Order Data</div>
                <textarea 
                    id="orderDataInput" 
                    class="paste-textarea" 
                    placeholder="Paste your Shopify order export here..."
                ></textarea>
            </div>

            <div class="action-buttons">
                <button class="btn btn-primary tooltip" onclick="generateStandardEmail()" data-tooltip="Generate standard confirmation email">
                    ✨ Standard
                </button>
            </div>
            <div class="action-buttons">
                <button class="btn btn-secondary tooltip" onclick="generateHighRiskEmail()" data-tooltip="Generate high-risk cancellation email">
                    🚨 High Risk
                </button>
            </div>
            <div class="action-buttons">
                <button class="btn btn-tertiary tooltip" onclick="generateReturnEmail()" data-tooltip="Generate return instructions email">
                    ↩️ Return
                </button>
            </div>
        </div>

        <!-- Main Mail Panel -->
        <div class="main-panel">
            <div class="section-title">
                <div class="section-icon">✉️</div>
                Compose Email
                <div id="statusIndicator" class="status-indicator" style="margin-left: auto; display: none;">
                    <div class="status-dot"></div>
                    Ready to Send
                </div>
            </div>

            <div class="mail-compose">
                <div class="compose-header">
                    <div class="form-group">
                        <label class="form-label" for="recipientEmail">To:</label>
                        <input 
                            type="email" 
                            id="recipientEmail" 
                            class="form-input" 
                            placeholder="Recipient email address"
                            readonly
                        >
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label" for="emailSubject">Subject:</label>
                        <input 
                            type="text" 
                            id="emailSubject" 
                            class="form-input" 
                            placeholder="Email subject line"
                            readonly
                        >
                    </div>
                </div>

                <div class="compose-body">
                    <label class="form-label" for="emailBody">Message:</label>
                    <textarea 
                        id="emailBody" 
                        class="body-textarea" 
                        placeholder="Email message will appear here..."
                        readonly
                    ></textarea>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Update date and time
        function updateDateTime() {
            const now = new Date();
            const dateOptions = { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            };
            const timeOptions = { 
                hour: '2-digit', 
                minute: '2-digit',
                second: '2-digit'
            };
            
            document.getElementById('currentDate').textContent = 
                now.toLocaleDateString('en-US', dateOptions);
            document.getElementById('currentTime').textContent = 
                now.toLocaleTimeString('en-US', timeOptions);
        }

        // Initialize and update every second
        updateDateTime();
        setInterval(updateDateTime, 1000);

        // Parse Shopify order data
        function parseShopifyData(rawText) {
            const data = {
                customer_name: "[Customer Name Not Found]",
                email_address: "[Email Not Found]",
                phone_number: "[Phone Not Found]",
                order_number: "[Order # Not Found]",
                items: [],
                missing_info: []
            };

            if (!rawText.trim()) {
                return data;
            }

            const lines = rawText.split('\n').map(line => line.trim()).filter(line => line);

            // Extract customer name
            const emailSentMatch = rawText.match(/Order confirmation email was sent to (.*?) \([\w\.-]+@[\w\.-]+\.[\w\.-]+\)/i);
            if (emailSentMatch) {
                data.customer_name = emailSentMatch[1].trim();
            } else {
                data.missing_info.push("Customer Name");
            }

            // Extract email
            const emailMatch = rawText.match(/[\w\.-]+@[\w\.-]+\.[\w\.-]+/);
            if (emailMatch) {
                data.email_address = emailMatch[0].trim();
            } else {
                data.missing_info.push("Email Address");
            }

            // Extract phone
            const phoneMatch = rawText.match(/(\+1[\s\-()]?\d{3}[\s\-()]?\d{3}[\s\-()]?\d{4}|\d{3}[\s\-()]?\d{3}[\s\-()]?\d{4})/);
            if (phoneMatch) {
                data.phone_number = phoneMatch[0].trim();
            } else {
                data.missing_info.push("Phone Number");
            }

            // Extract order number
            const orderMatch = rawText.match(/dazzlepremium#(\d+)/i);
            if (orderMatch) {
                data.order_number = orderMatch[1].trim();
            } else {
                data.missing_info.push("Order Number");
            }

            // Extract items (simplified)
            lines.forEach((line, index) => {
                if (line.includes(' - ') && !line.toLowerCase().includes('discount') && !line.toLowerCase().includes('total')) {
                    const parts = line.split(' - ');
                    if (parts.length >= 2) {
                        data.items.push({
                            product_name: parts[0].trim(),
                            style_code: parts[1].trim(),
                            size: "One Size",
                            quantity: 1
                        });
                    }
                }
            });

            if (data.items.length === 0) {
                data.missing_info.push("Order Items");
            }

            return data;
        }

        // Generate standard email
        function generateStandardEmail() {
            const rawText = document.getElementById('orderDataInput').value;
            const parsedData = parseShopifyData(rawText);
            
            updateMissingInfo(parsedData.missing_info);
            
            const subject = `Final Order Confirmation of dazzlepremium#${parsedData.order_number}`;
            
            let orderDetails = '';
            if (parsedData.items.length > 1) {
                parsedData.items.forEach((item, idx) => {
                    orderDetails += `- Item ${idx + 1}:\n`;
                    orderDetails += `•  Product: ${item.product_name}\n`;
                    orderDetails += `•  Style Code: ${item.style_code}\n`;
                    orderDetails += `•  Size: ${item.size}`;
                    if (item.quantity > 1) {
                        orderDetails += `\n•  Quantity: ${item.quantity}`;
                    }
                    orderDetails += '\n\n';
                });
            } else if (parsedData.items.length === 1) {
                const item = parsedData.items[0];
                orderDetails = `•  Product: ${item.product_name}\n•  Style Code: ${item.style_code}\n•  Size: ${item.size}`;
                if (item.quantity > 1) {
                    orderDetails += `\n•  Quantity: ${item.quantity}`;
                }
            } else {
                orderDetails = "No items found.";
            }

            const message = `Hello ${parsedData.customer_name},

This is DAZZLE PREMIUM Support confirming Order ${parsedData.order_number}

- Please reply YES to confirm just this order only.
- Kindly also reply YES to the SMS sent automatically to your inbox.

Order Details:
${orderDetails}

For your security, we use two-factor authentication. If this order wasn't placed by you, text us immediately at 410-381-0000 to cancel.

Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.

If you have any questions our US-based team is here Monday–Saturday, 10 AM–6 PM.
Thank you for choosing DAZZLE PREMIUM!`;

            populateEmailFields(parsedData.email_address, subject, message);
        }

        // Generate high-risk email
        function generateHighRiskEmail() {
            const rawText = document.getElementById('orderDataInput').value;
            const parsedData = parseShopifyData(rawText);
            
            updateMissingInfo(parsedData.missing_info);
            
            const subject = "Important: Your DAZZLE PREMIUM Order - Action Required";
            const message = `Hello ${parsedData.customer_name},

We hope this message finds you well.

We regret to inform you that your recent order has been automatically cancelled as it was flagged as a high-risk transaction by our system. This is a standard security measure to help prevent unauthorized or fraudulent activity.

If you would still like to proceed with your order, we'd be happy to assist you in placing it manually. To do so, we kindly ask that you transfer the payment via Cash App.

Once the payment is received, we will immediately process your order and provide confirmation along with tracking details.

If you have any questions or need assistance, feel free to reply to this email.

Thank you,
DAZZLE PREMIUM Support`;

            populateEmailFields(parsedData.email_address, subject, message);
        }

        // Generate return email
        function generateReturnEmail() {
            const rawText = document.getElementById('orderDataInput').value;
            const parsedData = parseShopifyData(rawText);
            
            updateMissingInfo(parsedData.missing_info);
            
            const subject = "DAZZLE PREMIUM: Your Return Request Instructions";
            const message = `Dear ${parsedData.customer_name},

Thank you for reaching out to us regarding your return request. To ensure a smooth and successful return process, please carefully follow the steps below:

1. Go to your local post office or any shipping carrier (USPS, FedEx, UPS, DHL).

2. Create and pay for the return shipping label.
(Please note: You are responsible for the return shipping cost.)

3. Ship the item to the following address:

Dazzle Premium 
3500 East-West Highway 
Suite 1032 
Hyattsville, MD 20782 
+1 (301) 942-0000 

4. Email us the tracking number after you ship the package by replying to this email.

Once we receive the returned item in its original condition with the tags intact and complete our inspection, we will process your refund.

If you have any questions, feel free to reply to this email.`;

            populateEmailFields(parsedData.email_address, subject, message);
        }

        // Update missing info display
        function updateMissingInfo(missingInfo) {
            const section = document.getElementById('missingInfoSection');
            const list = document.getElementById('missingInfoList');
            
            if (missingInfo.length > 0) {
                list.innerHTML = '';
                missingInfo.forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = item;
                    list.appendChild(li);
                });
                section.style.display = 'block';
            } else {
                section.style.display = 'none';
            }
        }

        // Populate email fields
        function populateEmailFields(email, subject, body) {
            document.getElementById('recipientEmail').value = email;
            document.getElementById('emailSubject').value = subject;
            document.getElementById('emailBody').value = body;
            document.getElementById('statusIndicator').style.display = 'flex';
        }

        // Copy to clipboard functionality
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                // Visual feedback could be added here
                console.log('Copied to clipboard');
            });
        }

        // Add double-click to copy functionality
        document.getElementById('recipientEmail').addEventListener('dblclick', function() {
            copyToClipboard(this.value);
        });

        document.getElementById('emailSubject').addEventListener('dblclick', function() {
            copyToClipboard(this.value);
        });

        document.getElementById('emailBody').addEventListener('dblclick', function() {
            copyToClipboard(this.value);
        });
    </script>
</body>
</html>
