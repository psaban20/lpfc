'use client';

export default function MarketingPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <iframe
            src="/LaPorte_FC_Marketing_Materials.html"
            className="w-full"
            style={{ height: 'calc(100vh - 120px)', minHeight: '800px' }}
            title="LaPorte FC Marketing Materials"
          />
        </div>
      </div>
    </div>
  );
}
