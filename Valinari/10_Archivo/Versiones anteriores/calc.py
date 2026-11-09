vals={'Valinor':13.75,'Tol Eressea':5.1,'Systreyjar':4.1,'Nosselie':7.9,'Numenor':5.644,'Venezuela':57.126,'Orinoco':27.19,'Sirename':16.15,'Panama':14.047,'Colombia':24.071,'Trinidad':3.5,'Tobago':.8,'Bermudas':.6,'Bahamas':1.306,'Barbados':1.6,'Malaca':28,'Hawaii':5.211,'Fiji':3.007,'Polinesia':4.3,'Micronesia':2.3}
scale=140.702/sum(vals.values())
print(scale, sum(vals.values()))
for k,v in vals.items(): print(k, round(v*scale,3))
print(sum(v*scale for v in vals.values()))
