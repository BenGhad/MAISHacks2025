import React from "react";

const Card = ({ title, description }) => {
  return (
    <div className="bg-white shadow-lg rounded-2xl p-6 max-w-sm">
      <h2 className="text-xl font-bold text-gray-900">{title}</h2>
      <p className="text-gray-600 mt-2">{description}</p>
    </div>
  );
};

export default Card;