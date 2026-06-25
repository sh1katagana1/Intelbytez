# Advisory - Agree to Steal

***

## Summary
The AgreeToSteal attack was discovered by Koi Security, and it targeted users of Microsoft Outlook via a malicious add-in. This add-in, once installed, granted the attacker access to the victim’s email credentials and emails.

## What happened?
AgreeTo was a real product. An open-source meeting scheduling tool with a Chrome extension (1,000 users, 4.71-star rating, 21 reviews) and an Outlook add-in published to Microsoft's store in December 2022. The developer maintained an active GitHub repo, then development stopped. The last Chrome extension update shipped in May 2023. The developer's domain, agreeto.app, expired. Google eventually removed the dead Chrome extension in February 2025. But the Outlook add-in stayed listed in Microsoft's Office Store, still pointing to a Vercel URL that no longer belonged to anyone.

At some point after the developer abandoned the project, their Vercel deployment was deleted. The subdomain outlook-one.vercel.app became claimable. An attacker grabbed it. They deployed a four-page phishing kit: a fake Microsoft sign-in page, a password collection page, an exfiltration script, and a redirect. They didn't submit anything to Microsoft. They weren't required to pass any review. They didn't create a store listing. The listing already existed, Microsoft-reviewed, Microsoft-signed, Microsoft-distributed. The attacker just claimed an orphaned URL, and Microsoft's infrastructure did the rest.

## What are Outlook Add-ins?
Outlook add-ins are small software extensions that enhance or modify the functionality of Microsoft Outlook. They are designed to integrate with the Outlook client (either the desktop application or the web-based version) to offer additional features, tools, or services that aren't included by default in Outlook. A good example is PhishAlert V2. 

Add-ins allow developers to extend Outlook's capabilities, enabling users to perform tasks directly within the Outlook interface, such as scheduling meetings, tracking emails, managing tasks, or integrating with other apps or services, like Phish Alert.

Outlook add-ins work by interacting with Outlook through a combination of web technologies (HTML, CSS, JavaScript) and Microsoft’s APIs (Application Programming Interfaces). Here’s a breakdown of how they operate:
1. Add-ins are typically distributed through the Microsoft Store or as custom add-ins in corporate environments. Users or administrators can install them directly within Outlook from the Office Store (for Outlook Web, Desktop, or Mobile) or via corporate deployment mechanisms (like Exchange Server or Microsoft 365 admin center). If you want to see yours, make a new email and look for an icon on the toolbar that looks like a box with 4 little boxes inside of it. This leads to managing your addins. 
2. Most Outlook add-ins are web-based and are essentially web applications that run inside Outlook. These add-ins are built using web technologies like HTML, JavaScript, and CSS. They are served from the cloud or a web server, allowing them to be easily updated or modified without needing the user to install new versions.
3. Every add-in must include a manifest file, which is an XML file that describes the add-in’s functionality, interface, permissions, and integration points. The manifest provides Outlook with the necessary details to install and run the add-in.
4. When an add-in is installed, it appears as a button or a panel within the Outlook interface, depending on its functionality.

Here are some examples of types of Add-ins you may see and what action makes them visible:
1. Message Read Add-ins: These add-ins interact with the content of emails you read. For example, they can add extra features like translating messages, highlighting important information, or integrating with third-party services like CRM tools.
2. Compose Add-ins: These add-ins work when you are writing a new message, enabling you to integrate additional features, such as adding attachments from cloud storage or using predefined templates.
3. Appointment Add-ins: These add-ins are designed to enhance the calendar function. They can automatically schedule meetings, set reminders, or sync appointments with external calendars.

Add-ins need permissions to access certain data in the user’s mailbox. For example, they might need permission to read emails, send messages, or create calendar events. These permissions are declared in the manifest file, and users are asked to approve them when the add-in is first installed. For the attack we are talking about today, the original manifest had Read-Write permissions, which means the new attacker owner also inherits these permissions.

The core of most add-ins is the web service. It’s a backend application that processes requests from the Outlook client (e.g., getting user data, sending emails, etc.). Developers usually write this backend using technologies like Node.js, ASP.NET, or Python. This backend service can interact with databases, external APIs, or other resources to provide functionality to the add-in. The add-in’s user interface is typically built using HTML and JavaScript. This UI can be displayed within Outlook in a task pane, dialog box, or as part of the message composing or reading experience.

## Attack Flow
When a victim opens the AgreeTo add-in in Outlook, they don't see a meeting scheduler. They see a Microsoft sign-in page.

![](https://cdn.prod.website-files.com/689ad8c5d13f40cf59df0e0c/698c696bff3dfb1afee92be2_86eb1fec.png)

They enter their email, then their password. A single JavaScript function collects the credentials along with the victim's IP address, and sends everything to the attacker via Telegram's Bot API. No command-and-control servers. No complex infrastructure. Just a fetch() call to Telegram. Then a loading spinner for a few seconds, and a seamless redirect to the real login.microsoftonline.com. The victim assumes they need to sign in again and goes about their day. They have no idea their password was just stolen.

![](https://cdn.prod.website-files.com/689ad8c5d13f40cf59df0e0c/698c696bff3dfb1afee92be5_71684b43.png)

The Koi researchers were able to gain access to the attackers exfil infrastructure and pull down what he stole. In all it was over 4000 victims, every email, every password, every credit card number, every intercepted security answer.

## Mitigations
1. Admin-Controlled Add-ins: Organizations should enforce the use of only approved and vetted add-ins in Outlook and other Microsoft 365 apps. Use Microsoft 365 admin controls (via Exchange Admin Center or Microsoft 365 Admin Center) to restrict and audit which add-ins can be installed by users. Only allow known, trusted add-ins through a corporate-controlled add-in catalog.
2. Disable Unnecessary Add-ins: Disable or remove any add-ins that are not critical to your organization's needs. This will reduce the attack surface significantly.
3. Restrict Add-in Permissions: Enforce policies that limit the permissions granted to add-ins (e.g., avoid granting full access to email or calendar events unless absolutely necessary).
4. Enforce Periodic Review: Implement processes to review the permissions and sources of all add-ins periodically to ensure they haven't changed or been compromised.
5. You can configure Intune to block the installation of unauthorized add-ins for Outlook.
6. App configuration policies for Outlook can be used to control which add-ins users can install.
7. You can restrict add-ins via Office 365 App Configuration Policies. This can ensure that only approved add-ins are available to users.
8. With App Protection Policies in Intune, you can limit the permissions granted to add-ins within Outlook. For instance, you can prevent add-ins from accessing sensitive corporate data, email content, or calendar events unless the add-in is trusted.
9. You can manage which permissions are granted to add-ins via Office 365 Management. This would help restrict access to sensitive data based on your organization’s policies.

Some example configurations:
1. Prevent add-ins that request high-level permissions (e.g., access to all email data, contacts, etc.).
2. Disallow external or unverified add-ins that require user authentication or connect to external URLs without approval.

## References
https://www.koi.ai/blog/agreetosteal-the-first-malicious-outlook-add-in-leads-to-4-000-stolen-credentials

## KQL
```
DeviceNetworkEvents
| where RemoteUrl contains "outlook-one.vercel.app"  // Phishing domain
| where ActionType == "ConnectionSuccess"            // Filter for successful connections
| project Timestamp, DeviceName, RemoteUrl, InitiatingProcessFileName, InitiatingProcessCommandLine, RemotePort, ActionType


DeviceProcessEvents
| where InitiatingProcessFileName == "Outlook.exe"  // Filter for Outlook-related processes
| where ProcessCommandLine contains "WA200004949"  // Filter for the malicious Add-in ID
| project Timestamp, DeviceName, FileName, ProcessCommandLine, InitiatingProcessFileName, ActionType

```




















 







