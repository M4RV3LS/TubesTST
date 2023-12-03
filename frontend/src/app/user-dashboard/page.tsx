// pages/user-dashboard.tsx
"use client";
import React from "react";

const UserDashboard = () => {
  const handleLogout = () => {
    localStorage.removeItem("token");
    // Redirect to the login page
    window.location.href = "/login";
  };

  return (
    <div>
      <div>ini page user dashboard</div>
      <button onClick={handleLogout} className="bg-red-800 text-white">
        Logout
      </button>
    </div>
  );
};

export default UserDashboard;
