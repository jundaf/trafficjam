#include <cmath>
#include <array>
#include <iostream>

using namespace std;

#define _MIN_SIN_ABS_ 0.5f
#define LAT_LON_SCALE 1
#define EPSILON 1

struct Vector2
{
	//const static VertexFormat format = VertexFormat_xy;
	float x, y;
	inline void normalize() {
		float ld = 1 / sqrt(x * x + y * y);
		x = x * ld;
		y = y * ld;
	}
	inline void normalize(float length) {
		float ld = 1 / length;
		x = x * ld;
		y = y * ld;
	}
	inline float length() {
		return sqrt(x * x + y * y);
	}
	inline float lengthSquared() {
		return x * x + y * y;
	}

	static float dotProduct(const Vector2* v1, const Vector2* v2)
	{
		return ( v1->x * v2->x + v1->y * v2->y );
	}

	class Converter
	{
	public:
		inline Vector2 fromVector2(const Vector2& p) {
			return p;
		}
	};
};

static void _thickLineStripeCalculateJoints( const Vector2* p1_, const Vector2* p2_, const Vector2* p3_, Vector2* p4, float halfWidth)
{
	Vector2 v21, v23;
	Vector2 v24;

	float cosA, sinA;
	float l;

	v21.x = p1_->x - p2_->x;
	v21.y = (p1_->y - p2_->y);
	v21.normalize();

	v23.x = p3_->x - p2_->x;
	v23.y = (p3_->y - p2_->y);
	v23.normalize();

	v24.x = (v23.x + v21.x) / 2;
	v24.y = (v23.y + v21.y) / 2;

	if (v24.lengthSquared() < EPSILON)
	{
		//(v21.y, -v21.x) is also OK, since later sinA<0 will cause the 'l' be inverted.
		v24.x = -v21.y;
		v24.y = v21.x;
	}
	else
	{
		v24.normalize();
	}

	sinA = v21.x*v24.y - v24.x*v21.y;
	float sinAAbs = abs(sinA);
	if (sinAAbs < _MIN_SIN_ABS_)
		sinAAbs = _MIN_SIN_ABS_;

	if (sinA >= 0)
		l = halfWidth / sinAAbs;
	else  
		l = -halfWidth / sinAAbs;

	p4->x = p2_->x + l * v24.x * LAT_LON_SCALE;
	p4->y = p2_->y + l * v24.y;
}

void lineRightShift(Vector2* points, size_t num, float shift)
{
	Vector2 head, tail, lastShifted, shifted;

	if (num < 2)
		return;

	Vector2* p1 = points;
	Vector2* p2 = p1 + 1;
	Vector2* p3 = p2 + 1;
	Vector2* pEnd = &points[num];

	head.x = p1->x - (p2->x - p1->x);
	head.y = p1->y - (p2->y - p1->y);
	_thickLineStripeCalculateJoints(&head, p1, p2, &lastShifted, shift);

	for(; p3 < pEnd; p1++, p2++, p3++)
	{
		_thickLineStripeCalculateJoints(p1, p2, p3, &shifted, shift);
		*p1 = lastShifted;
		lastShifted = shifted;
	}

	tail.x = p2->x - (p1->x - p2->x);
	tail.y = p2->y - (p1->y - p2->y);
	_thickLineStripeCalculateJoints(p1, p2, &tail, &shifted, shift);
	*p1 = lastShifted;
	*p2 = shifted;
}

template<size_t N>
void show_vectors(const array<Vector2, N> &av)
{
	for (auto v: av) {
		cout << v.x << ',' << v.y << ';';
	}
	cout << endl;
}

int main(int argc, char const *argv[])
{
	array<Vector2, 20> a1, a2;

	for (int i; i < 20; i++) {
		a1[i].x = i * 5.0;
		a1[i].y = 50.0;
		a2[i].x = i * 5.0;
		a2[i].y = 60.0;
	}

	show_vectors(a1);
	lineRightShift(a1.data(), a1.size(), 5.0);
	show_vectors(a1);

	cout << endl;
	show_vectors(a2);
	lineRightShift(a2.data(), a2.size(), 5.0);
	show_vectors(a2);

	return 0;
}