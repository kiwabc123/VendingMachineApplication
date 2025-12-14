import ProductCard from "./ProductCard.jsx";

export default function VendingScreen({ products, onSelect, loading }) {
    // Group products by category (first letter of slot_no)
    const groupedProducts = products.reduce((acc, product) => {
        const category = product.slot_no.charAt(0); // A, B, C
        if (!acc[category]) {
            acc[category] = [];
        }
        acc[category].push(product);
        return acc;
    }, {});

    const getCategoryName = (category) => {
        switch (category) {
            case 'A': return '🥤 Drinks';
            case 'B': return '🍿 Snacks';
            case 'C': return '🥜 Nuts';
            default: return 'Other';
        }
    };

    return (
        <div className="h-full">

            <div className="h-full overflow-y-auto space-y-6">
                {Object.keys(groupedProducts).sort().map(category => (
                    <div key={category} className="space-y-3">
                        <h2 className="text-xl font-heading text-cafe-primary border-b border-cafe-primary/20 pb-2">
                            {getCategoryName(category)}
                        </h2>
                        <div
                            className="
                            grid
                            grid-cols-2
                            sm:grid-cols-3
                            md:grid-cols-4
                            lg:grid-cols-5
                            xl:grid-cols-6
                            gap-4
                        "
                        >
                            {groupedProducts[category].map(p => (
                                <ProductCard
                                    key={p.id}
                                    {...p}
                                    onSelect={() => onSelect(p)}
                                    loading={loading}
                                />
                            ))}
                        </div>

                    </div>
                ))}
            </div>
        </div>
    );
}
