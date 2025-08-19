<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mail - DAZZLE PREMIUM</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        /* Custom scrollbar for a more polished look */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        .placeholder-text {
            color: #9ca3af; /* gray-400 */
        }
    </style>
</head>
<body class="bg-gray-100 text-gray-800">

    <div class="container mx-auto p-4 md:p-8">
        <!-- Header Section -->
        <header class="mb-6">
            <h1 class="text-4xl font-bold text-gray-900">📧 Mail - DAZZLE PREMIUM</h1>
            <p class="text-lg text-gray-600 mt-1">Premium Email Generator</p>
            <div id="datetime-display" class="mt-4 text-sm bg-blue-100 text-blue-800 p-3 rounded-lg inline-block">
                <!-- Date and time will be injected here by JavaScript -->
            </div>
        </header>

        <!-- Main Content Grid -->
        <main class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Left Column: Input and Actions -->
            <div class="bg-white p-6 rounded-xl shadow-md flex flex-col space-y-6">
                <div>
                    <h2 class="text-xl font-semibold mb-2">📋 Paste Shopify Order Data</h2>
                    <textarea id="order-input" class="w-full h-80 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out font-mono text-sm" placeholder="Paste your full Shopify order page content here..."></textarea>
                </div>

                <!-- Missing Info Display -->
                <div id="missing-info-container" class="hidden">
                    <div class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-800 p-4 rounded-r-lg">
                        <h4 class="font-bold">⚠️ Missing Information</h4>
                        <ul id="missing-info-list" class="list-disc list-inside mt-2 text-sm">
                            <!-- Missing items will be listed here -->
                        </ul>
                    </div>
                </div>

                <div>
                    <h2 class="text-xl font-semibold mb-3">✨ Generate Email</h2>
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                        <button id="btn-standard" class="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150 ease-in-out shadow-sm disabled:bg-gray-400 disabled:cursor-not-allowed" disabled>✨ Standard</button>
                        <button id="btn-medium-risk" class="w-full bg-yellow-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition duration-150 ease-in-out shadow-sm disabled:bg-gray-400 disabled:cursor-not-allowed" disabled>🔶 Medium Risk</button>
                        <button id="btn-high-risk" class="w-full bg-red-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition duration-150 ease-in-out shadow-sm disabled:bg-gray-400 disabled:cursor-not-allowed" disabled>🚨 High Risk</button>
                        <button id="btn-return" class="w-full bg-gray-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition duration-150 ease-in-out shadow-sm disabled:bg-gray-400 disabled:cursor-not-allowed" disabled>↩️ Return</button>
                    </div>
                </div>

                <!-- Order Notes Section -->
                <div id="order-notes-section" class="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-r-lg">
                    <h3 id="notes-header" class="text-lg font-semibold text-blue-900 mb-2">📝 Notes for Order: [No Order]</h3>
                    <textarea id="order-notes-textarea" class="w-full h-32 p-3 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out text-sm" placeholder="e.g., 'Follow-up needed', 'Called customer about size issue'"></textarea>
                </div>
            </div>

            <!-- Right Column: Compose Email -->
            <div class="bg-white p-6 rounded-xl shadow-md flex flex-col space-y-4">
                <h2 class="text-xl font-semibold">✉️ Compose Email</h2>
                
                <!-- Success Message -->
                <div id="success-message" class="hidden bg-green-100 border-l-4 border-green-500 text-green-800 p-4 rounded-r-lg">
                    <strong class="font-semibold">✅ Email Generated Successfully!</strong>
                </div>
                
                <!-- Placeholder View -->
                <div id="placeholder-view">
                    <div class="bg-gray-50 p-4 rounded-lg text-center placeholder-text">
                        👆 Paste order data and select an email type to generate the content.
                    </div>
                    <div class="mt-4 space-y-4">
                        <input type="text" placeholder="Recipient email will appear here" class="w-full p-3 bg-gray-100 border border-gray-300 rounded-lg cursor-not-allowed" disabled>
                        <input type="text" placeholder="Email subject will appear here" class="w-full p-3 bg-gray-100 border border-gray-300 rounded-lg cursor-not-allowed" disabled>
                        <textarea placeholder="Email message will appear here..." class="w-full h-96 p-3 bg-gray-100 border border-gray-300 rounded-lg cursor-not-allowed" disabled></textarea>
                    </div>
                </div>

                <!-- Generated Email View -->
                <div id="generated-view" class="hidden space-y-4">
                     <div>
                        <label for="email-to" class="block text-sm font-medium text-gray-700 mb-1">To:</label>
                        <input type="text" id="email-to" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition">
                     </div>
                     <div>
                        <label for="email-subject" class="block text-sm font-medium text-gray-700 mb-1">Subject:</label>
                        <input type="text" id="email-subject" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition">
                     </div>
                     <div>
                        <label for="email-body" class="block text-sm font-medium text-gray-700 mb-1">Message:</label>
                        <textarea id="email-body" class="w-full h-96 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"></textarea>
                     </div>
                </div>
            </div>
        </main>
        
        <!-- Footer -->
        <footer class="text-center mt-8 py-4 border-t border-gray-200">
            <p class="text-sm text-gray-600"><strong>DAZZLE PREMIUM</strong> - Premium Email Management System</p>
        </footer>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            // --- STATE MANAGEMENT ---
            const state = {
                parsedData: null,
                isDataAvailable: false,
                orderNotes: {}, // Keyed by order number
            };

            // --- DOM ELEMENT REFERENCES ---
            const orderInput = document.getElementById('order-input');
            const missingInfoContainer = document.getElementById('missing-info-container');
            const missingInfoList = document.getElementById('missing-info-list');
            const btnStandard = document.getElementById('btn-standard');
            const btnMediumRisk = document.getElementById('btn-medium-risk');
            const btnHighRisk = document.getElementById('btn-high-risk');
            const btnReturn = document.getElementById('btn-return');
            const notesHeader = document.getElementById('notes-header');
            const notesTextarea = document.getElementById('order-notes-textarea');
            const successMessage = document.getElementById('success-message');
            const placeholderView = document.getElementById('placeholder-view');
            const generatedView = document.getElementById('generated-view');
            const emailTo = document.getElementById('email-to');
            const emailSubject = document.getElementById('email-subject');
            const emailBody = document.getElementById('email-body');
            const datetimeDisplay = document.getElementById('datetime-display');

            // --- PARSING LOGIC ---
            function parseShopifyData(rawText) {
                const data = {
                    customer_name: "[Customer Name Not Found]",
                    email_address: "[Email Not Found]",
                    phone_number: "[Phone Not Found]",
                    order_number: "[Order # Not Found]",
                    items: [],
                    missing_info: []
                };

                if (!rawText || !rawText.trim()) return null;

                // Extract customer name
                let nameMatch = rawText.match(/Order confirmation email was sent to (.*?)\s*\(/i);
                if (nameMatch) {
                    data.customer_name = nameMatch[1].trim();
                } else {
                    let nameFallbackMatch = rawText.match(/Customer\n\n(.*?)\n/);
                    if (nameFallbackMatch) {
                        data.customer_name = nameFallbackMatch[1].trim();
                    } else {
                        data.missing_info.push("Customer Name");
                    }
                }

                // Extract email
                let emailMatch = rawText.match(/[\w\.-]+@[\w\.-]+\.[\w\.-]+/);
                if (emailMatch) {
                    data.email_address = emailMatch[0].trim();
                } else {
                    data.missing_info.push("Email Address");
                }

                // Extract phone
                let phoneMatch = rawText.match(/\+1[ \d\-()]{10,}/);
                if (phoneMatch) {
                    data.phone_number = phoneMatch[0].trim();
                } else {
                    data.missing_info.push("Phone Number");
                }

                // Extract order number
                let orderMatch = rawText.match(/dazzlepremium#(\d+)/i);
                if (orderMatch) {
                    data.order_number = orderMatch[1].trim();
                } else {
                    data.missing_info.push("Order Number");
                }

                // Extract items
                const lines = rawText.split('\n').map(line => line.trim());
                for (let i = 0; i < lines.length; i++) {
                    if (lines[i].startsWith("SKU:") && i > 1 && i < lines.length - 1) {
                        try {
                            const productLine = lines[i - 2];
                            const sizeLine = lines[i - 1];
                            const quantityLine = lines[i + 1];

                            const productMatch = productLine.match(/(.*) - (.*)/);
                            const productName = productMatch ? productMatch[1].trim() : productLine;
                            const styleCode = productMatch ? productMatch[2].trim() : "[Style Code Not Found]";

                            const size = sizeLine.includes('/') ? sizeLine.split('/')[0].trim() : sizeLine;

                            const quantityMatch = quantityLine.match(/×\s*(\d+)/);
                            const quantity = quantityMatch ? parseInt(quantityMatch[1], 10) : 1;

                            data.items.push({
                                product_name: productName,
                                style_code: styleCode,
                                size: size,
                                quantity: quantity
                            });
                        } catch (e) {
                            console.error("Error parsing an item, skipping.", e);
                            continue;
                        }
                    }
                }
                
                if (data.items.length === 0) {
                    data.missing_info.push("Order Items");
                }

                return data;
            }

            // --- EMAIL GENERATION LOGIC ---
            function generateEmailContent(parsedData, emailType) {
                let subject = "";
                let message = "";
                const to = parsedData.email_address;

                switch (emailType) {
                    case "standard":
                        subject = `Final Order Confirmation of dazzlepremium#${parsedData.order_number}`;
                        let orderDetails = parsedData.items.map((item, idx) => {
                            let detail = `- Item ${idx + 1}:\n`;
                            detail += `•  Product: ${item.product_name}\n`;
                            detail += `•  Style Code: ${item.style_code}\n`;
                            detail += `•  Size: ${item.size}`;
                            if (item.quantity > 1) {
                                detail += `\n•  Quantity: ${item.quantity}`;
                            }
                            return detail;
                        }).join('\n\n') || "No items found.";

                        message = `Hello ${parsedData.customer_name},\n\nThis is DAZZLE PREMIUM Support confirming Order ${parsedData.order_number}\n\n- Please reply YES to confirm just this order only.\n- Kindly also reply YES to the SMS sent automatically to your inbox.\n\nOrder Details:\n${orderDetails}\n\nFor your security, we use two-factor authentication. If this order wasn't placed by you, text us immediately at 410-381-0000 to cancel.\n\nNote: Any order confirmed after 3:00 pm will be scheduled for the next business day.\n\nIf you have any questions our US-based team is here Monday–Saturday, 10 AM–6 PM.\nThank you for choosing DAZZLE PREMIUM!`;
                        break;
                    
                    case "medium_risk":
                        subject = `Action Required: Please Verify Your DAZZLE PREMIUM Order #${parsedData.order_number}`;
                        let orderDetailsMediumRisk = parsedData.items.map(item => {
                            let detail = `• Product: ${item.product_name}\n`;
                            detail += `• Style Code: ${item.style_code}\n`;
                            detail += `• Size: ${item.size}`;
                            if (item.quantity > 1) {
                                detail += ` (Quantity: ${item.quantity})`;
                            }
                            return detail;
                        }).join('\n\n') || "No items found.";

                        message = `Hello ${parsedData.customer_name},\n\nThank you for shopping with DAZZLE PREMIUM.\n\nOur system has flagged your recent order (#${parsedData.order_number}) for additional verification. For your security and to prevent fraudulent activity, we are unable to ship this order until it has been manually reviewed and confirmed.\n\nOrder Details:\n${orderDetailsMediumRisk}\n\nTo complete verification, please reply to this email with:\n\n    Your Order Number\n\n    A valid photo ID (you may cover sensitive information, but your name must be visible)\n\n    A picture of the payment card used (you may cover all digits except the last 4)\n\nOnce we receive this information, our fraud prevention team will promptly review it and proceed with shipping.\n\nFor your security: If you did not place this order, please text us immediately at 410-381-0000 so we can cancel and secure your account.\n\nNote: Any order confirmed after 3:00 PM will be scheduled for the next business day.\n\nIf you have any questions, our US-based team is available Monday–Saturday, 10 AM–6 PM.\n\nWe truly value your safety and appreciate your cooperation.\nThank you for choosing DAZZLE PREMIUM!`;
                        break;

                    case "high_risk":
                        subject = "Important: Your DAZZLE PREMIUM Order - Action Required";
                        message = `Hello ${parsedData.customer_name},\n\nWe hope this message finds you well.\n\nWe regret to inform you that your recent order has been automatically cancelled as it was flagged as a high-risk transaction by our system. This is a standard security measure to help prevent unauthorized or fraudulent activity.\n\nIf you would still like to proceed with your order, we'd be happy to assist you in placing it manually. To do so, we kindly ask that you transfer the payment via Cash App.\n\nOnce the payment is received, we will immediately process your order and provide confirmation along with tracking details.\n\nIf you have any questions or need assistance, feel feel to reply to this email.\n\nThank you,\nDAZZLE PREMIUM Support`;
                        break;

                    case "return":
                        subject = "DAZZLE PREMIUM: Your Return Request Instructions";
                        message = `Dear ${parsedData.customer_name},\n\nThank you for reaching out to us regarding your return request. To ensure a smooth and successful return process, please carefully follow the steps below:\n\n1. Go to your local post office or any shipping carrier (USPS, FedEx, UPS, DHL).\n\n2. Create and pay for the return shipping label.\n(Please note: You are responsible for the return shipping cost.)\n\n3. Ship the item to the following address:\n\nDazzle Premium\n3500 East-West Highway\nSuite 1032\nHyattsville, MD 20782\n+1 (301) 942-0000\n\n4. Email us the tracking number after you ship the package by replying to this email.\n\nOnce we receive the returned item in its original condition with the tags intact and complete our inspection, we will process your refund.\n\nIf you have any questions, feel free to reply to this email.`;
                        break;
                }
                return { to, subject, message };
            }

            // --- UI UPDATE FUNCTIONS ---
            function updateDateTime() {
                const now = new Date();
                const optionsDate = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
                const optionsTime = { hour: 'numeric', minute: '2-digit', second: '2-digit', hour12: true };
                const dateString = now.toLocaleDateString('en-US', optionsDate);
                const timeString = now.toLocaleTimeString('en-US', optionsTime);
                datetimeDisplay.innerHTML = `📅 ${dateString} | 🕒 ${timeString}`;
            }

            function resetUI() {
                // Reset compose view
                placeholderView.classList.remove('hidden');
                generatedView.classList.add('hidden');
                successMessage.classList.add('hidden');
                
                // Reset missing info
                missingInfoContainer.classList.add('hidden');
                missingInfoList.innerHTML = '';

                // Disable buttons
                [btnStandard, btnMediumRisk, btnHighRisk, btnReturn].forEach(btn => btn.disabled = true);

                // Reset notes
                notesHeader.textContent = '📝 Notes for Order: [No Order]';
                notesTextarea.value = '';
            }

            function handleParse() {
                const rawText = orderInput.value;
                state.parsedData = parseShopifyData(rawText);
                state.isDataAvailable = !!state.parsedData;
                
                // Always reset the email view on new input
                placeholderView.classList.remove('hidden');
                generatedView.classList.add('hidden');
                successMessage.classList.add('hidden');

                if (state.isDataAvailable) {
                    // Enable buttons
                    [btnStandard, btnMediumRisk, btnHighRisk, btnReturn].forEach(btn => btn.disabled = false);
                    
                    // Display missing info if any
                    if (state.parsedData.missing_info.length > 0) {
                        missingInfoList.innerHTML = state.parsedData.missing_info.map(item => `<li>${item}</li>`).join('');
                        missingInfoContainer.classList.remove('hidden');
                    } else {
                        missingInfoContainer.classList.add('hidden');
                    }

                    // Update and load notes
                    const orderNum = state.parsedData.order_number || "[No Order]";
                    notesHeader.textContent = `📝 Notes for Order: ${orderNum}`;
                    notesTextarea.value = state.orderNotes[orderNum] || '';

                } else {
                    if (rawText.trim() === '') {
                        resetUI();
                    } else {
                        // There's text, but it couldn't be parsed
                        [btnStandard, btnMediumRisk, btnHighRisk, btnReturn].forEach(btn => btn.disabled = true);
                        missingInfoList.innerHTML = '<li>Could not parse any valid order data. Please check the pasted content.</li>';
                        missingInfoContainer.classList.remove('hidden');
                    }
                }
            }
            
            function handleGenerateEmail(emailType) {
                if (!state.isDataAvailable) {
                    // Flash the input border to indicate an issue
                    orderInput.classList.add('border-red-500', 'ring-red-500');
                    setTimeout(() => {
                        orderInput.classList.remove('border-red-500', 'ring-red-500');
                    }, 1500);
                    return;
                }
                
                const { to, subject, message } = generateEmailContent(state.parsedData, emailType);
                
                emailTo.value = to;
                emailSubject.value = subject;
                emailBody.value = message;

                placeholderView.classList.add('hidden');
                generatedView.classList.remove('hidden');
                successMessage.classList.remove('hidden');
            }
            
            // --- EVENT LISTENERS ---
            orderInput.addEventListener('input', handleParse);
            
            btnStandard.addEventListener('click', () => handleGenerateEmail('standard'));
            btnMediumRisk.addEventListener('click', () => handleGenerateEmail('medium_risk'));
            btnHighRisk.addEventListener('click', () => handleGenerateEmail('high_risk'));
            btnReturn.addEventListener('click', () => handleGenerateEmail('return'));
            
            notesTextarea.addEventListener('input', () => {
                if (state.isDataAvailable) {
                    const orderNum = state.parsedData.order_number;
                    if (orderNum) {
                        state.orderNotes[orderNum] = notesTextarea.value;
                    }
                }
            });

            // --- INITIALIZATION ---
            updateDateTime();
            setInterval(updateDateTime, 1000); // Update time every second
        });
    </script>
</body>
</html>
