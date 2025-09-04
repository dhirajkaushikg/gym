import React from 'react';

const TestComponent: React.FC = () => {
  return (
    <div className="p-4 bg-blue-500 text-white rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-2">Tailwind CSS Test</h2>
      <p className="mb-4">If this text is styled with a blue background, Tailwind CSS is working correctly.</p>
      <div className="bg-white text-blue-500 p-3 rounded">
        This should have a white background with blue text.
      </div>
    </div>
  );
};

export default TestComponent;