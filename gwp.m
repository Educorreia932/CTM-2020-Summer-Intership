[M1, M2, M3] = ndgrid(0:4);
m1 = M1(:); m2 = M2(:); m3 = M3(:);
solidx = find(all([m1 + m2 + m3 == 4, 9 <= m1+ 2* m2+ 3* m3, m1+ 2* m2+ 3* m3 <= 12, m3 >=2, m3+m2 >=3], 2));
[m1(solidx), m2(solidx), m3(solidx)]