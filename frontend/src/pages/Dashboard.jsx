import React from 'react';
import FileExplorer from './FileExplorer';

function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-4">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-100">File Manager</h1>
        {/* TODO: Tambahkan komponen file/folder explorer di sini */}
        <FileExplorer />
      </div>
    </div>
  );
}

export default Dashboard; 