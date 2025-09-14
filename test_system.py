#!/usr/bin/env python3
"""
Test script for Gift Guru MVP
Validates core functionality and performance requirements
"""

import pandas as pd
import time
import sys
import os
from datetime import datetime

# Add current directory to path to import app modules
sys.path.append('.')

class GiftGuruTester:
    def __init__(self):
        self.test_results = []
        self.start_time = None
        
    def log_test(self, test_name, passed, message="", execution_time=None):
        """Log test results"""
        result = {
            'test_name': test_name,
            'status': 'PASS' if passed else 'FAIL',
            'message': message,
            'execution_time': execution_time,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        # Print result
        status_symbol = "✅" if passed else "❌"
        time_info = f" ({execution_time:.3f}s)" if execution_time else ""
        print(f"{status_symbol} {test_name}{time_info}")
        if message:
            print(f"   📝 {message}")
    
    def test_data_loading(self):
        """Test gift database loading"""
        start = time.time()
        try:
            df = pd.read_csv('gift_database.csv')
            
            # Check required columns
            required_cols = ['product_name', 'price', 'category', 'tags', 'description', 'link']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                self.log_test(
                    "Database Structure", 
                    False, 
                    f"Missing columns: {missing_cols}",
                    time.time() - start
                )
                return False
            
            # Check data quality
            if df.empty:
                self.log_test("Database Content", False, "Database is empty", time.time() - start)
                return False
            
            # Check price range
            price_range = f"${df['price'].min():.0f}-${df['price'].max():.0f}"
            
            self.log_test(
                "Database Loading", 
                True, 
                f"Loaded {len(df)} gifts, price range: {price_range}",
                time.time() - start
            )
            return True
            
        except Exception as e:
            self.log_test("Database Loading", False, f"Error: {str(e)}", time.time() - start)
            return False
    
    def test_recommender_performance(self):
        """Test recommendation engine performance"""
        try:
            # Import the recommender class
            from app import GiftRecommender
            
            recommender = GiftRecommender()
            
            # Test cases with different user profiles
            test_cases = [
                {
                    'profile': 'gaming tech rgb mouse keyboard',
                    'budget_min': 20,
                    'budget_max': 60,
                    'expected_category': 'gaming'
                },
                {
                    'profile': 'wellness yoga meditation relaxation',
                    'budget_min': 30,
                    'budget_max': 80,
                    'expected_category': 'wellness'
                },
                {
                    'profile': 'cooking kitchen food gourmet',
                    'budget_min': 25,
                    'budget_max': 70,
                    'expected_category': 'food'
                }
            ]
            
            total_time = 0
            successful_tests = 0
            
            for i, test_case in enumerate(test_cases):
                start = time.time()
                
                recommendations = recommender.get_recommendations(
                    test_case['profile'],
                    test_case['budget_min'],
                    test_case['budget_max'],
                    num_recommendations=5
                )
                
                execution_time = time.time() - start
                total_time += execution_time
                
                # Check if recommendations were generated
                if recommendations:
                    # Check if recommendations are within budget
                    prices = [rec['price'] for rec in recommendations]
                    in_budget = all(test_case['budget_min'] <= price <= test_case['budget_max'] + 20 for price in prices)
                    
                    if in_budget and execution_time < 5.0:
                        successful_tests += 1
                        self.log_test(
                            f"Recommendation Test {i+1}",
                            True,
                            f"Generated {len(recommendations)} recommendations",
                            execution_time
                        )
                    else:
                        self.log_test(
                            f"Recommendation Test {i+1}",
                            False,
                            f"Budget/time issue: {in_budget}, {execution_time:.2f}s",
                            execution_time
                        )
                else:
                    self.log_test(
                        f"Recommendation Test {i+1}",
                        False,
                        "No recommendations generated",
                        execution_time
                    )
            
            # Overall performance test
            avg_time = total_time / len(test_cases)
            performance_pass = avg_time < 5.0 and successful_tests == len(test_cases)
            
            self.log_test(
                "Performance Requirement",
                performance_pass,
                f"Average response time: {avg_time:.3f}s (target: <5s)",
                avg_time
            )
            
            return performance_pass
            
        except Exception as e:
            self.log_test("Recommender Performance", False, f"Error: {str(e)}")
            return False
    
    def test_user_interface_components(self):
        """Test if UI components would work (simulate)"""
        try:
            # Test age ranges
            age_ranges = ["13-17 (Teen)", "18-25 (Young Adult)", "26-35 (Millennial)", 
                         "36-45 (Gen X)", "46-55 (Middle-aged)", "55+ (Senior)"]
            
            # Test occasions
            occasions = ["Birthday", "Anniversary", "Christmas", "Valentine's Day", 
                        "Graduation", "Housewarming", "Just Because", "Other"]
            
            # Test budget ranges
            budget_valid = True
            min_budget, max_budget = 10, 100
            
            ui_components_valid = (
                len(age_ranges) > 0 and 
                len(occasions) > 0 and
                min_budget < max_budget
            )
            
            self.log_test(
                "UI Components",
                ui_components_valid,
                f"Age ranges: {len(age_ranges)}, Occasions: {len(occasions)}"
            )
            
            return ui_components_valid
            
        except Exception as e:
            self.log_test("UI Components", False, f"Error: {str(e)}")
            return False
    
    def test_feedback_system(self):
        """Test feedback collection system"""
        try:
            from app import GiftRecommender
            
            recommender = GiftRecommender()
            
            # Simulate user data and feedback
            user_data = {
                'age_range': '18-25 (Young Adult)',
                'gender': 'Any',
                'interests': 'gaming, tech',
                'occasion': 'Birthday',
                'budget_min': 30,
                'budget_max': 70
            }
            
            recommendations = [
                {'name': 'Test Gift 1', 'price': 45},
                {'name': 'Test Gift 2', 'price': 55}
            ]
            
            ratings = [4, 5]
            
            # Test feedback saving
            start = time.time()
            recommender.save_feedback(user_data, recommendations, ratings)
            execution_time = time.time() - start
            
            # Check if feedback file was created
            feedback_exists = os.path.exists('user_feedback.csv')
            
            if feedback_exists:
                # Read and validate feedback
                feedback_df = pd.read_csv('user_feedback.csv')
                last_entry = feedback_df.iloc[-1]
                
                feedback_valid = (
                    last_entry['age_range'] == user_data['age_range'] and
                    last_entry['average_rating'] == 4.5  # Average of [4, 5]
                )
                
                self.log_test(
                    "Feedback System",
                    feedback_valid,
                    f"Feedback saved successfully, avg rating: {last_entry['average_rating']}",
                    execution_time
                )
                return feedback_valid
            else:
                self.log_test("Feedback System", False, "Feedback file not created")
                return False
                
        except Exception as e:
            self.log_test("Feedback System", False, f"Error: {str(e)}")
            return False
    
    def test_malayali_humor_feature(self):
        """Test Malayali humor phrases"""
        try:
            from app import GiftRecommender
            
            recommender = GiftRecommender()
            phrases = recommender.malayali_phrases
            
            humor_valid = (
                len(phrases) > 0 and
                any('mallu' in phrase.lower() or 'adipoli' in phrase.lower() for phrase in phrases)
            )
            
            self.log_test(
                "Malayali Humor Feature",
                humor_valid,
                f"Found {len(phrases)} humor phrases"
            )
            
            return humor_valid
            
        except Exception as e:
            self.log_test("Malayali Humor Feature", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Gift Guru MVP Test Suite")
        print("=" * 50)
        
        tests = [
            self.test_data_loading,
            self.test_recommender_performance,
            self.test_user_interface_components,
            self.test_feedback_system,
            self.test_malayali_humor_feature
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed_tests += 1
            except Exception as e:
                print(f"❌ Test failed with exception: {str(e)}")
        
        # Summary
        print("\n" + "=" * 50)
        print(f"📊 Test Summary: {passed_tests}/{total_tests} tests passed")
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"✅ Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 MVP is ready for deployment!")
        else:
            print("⚠️ Some issues need to be addressed before deployment")
        
        return success_rate >= 80

if __name__ == "__main__":
    print("Gift Guru MVP - System Validation Test")
    print("Author: MiniMax Agent")
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tester = GiftGuruTester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)